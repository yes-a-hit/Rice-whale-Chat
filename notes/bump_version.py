"""
版本号工具：遵循 1.x.y-tag.z

用法：
    python notes/bump_version.py            # 看当前版本
    python notes/bump_version.py tag        # 1.0.0-alpha.1 -> 1.0.0-alpha.2（同 tag 递增 z）
    python notes/bump_version.py patch      # 1.0.0-alpha.2 -> 1.0.1-alpha.1（y+1，z 归 1）
    python notes/bump_version.py minor      # 1.0.1-alpha.1 -> 1.1.0-alpha.1
    python notes/bump_version.py stable     # 1.1.0-alpha.1 -> 1.1.0（正式版，不带 tag）
    python notes/bump_version.py alpha      # 1.1.0 -> 1.1.0-alpha.1
    python notes/bump_version.py beta       # 1.1.0 -> 1.1.0-beta.1

versionCode 由 android/app/build.gradle 从 package.json 计算：
    major*1000000 + minor*10000 + patch*100 + tag 序号（正式版序号为 0）
"""

import io
import pathlib
import re
import sys

PKG = pathlib.Path(__file__).resolve().parent.parent / "package.json"
PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-([A-Za-z]+)\.(\d+))?$")


def parse(version: str) -> dict:
    m = PATTERN.match(version)
    if not m:
        raise SystemExit(f"版本号不符合 1.x.y-tag.z：{version}")
    return {
        "major": int(m.group(1)),
        "minor": int(m.group(2)),
        "patch": int(m.group(3)),
        "tag": m.group(4),
        "n": int(m.group(5)) if m.group(5) else 0,
    }


def render(v: dict) -> str:
    base = f"{v['major']}.{v['minor']}.{v['patch']}"
    return f"{base}-{v['tag']}.{v['n']}" if v["tag"] else base


def version_code(v: dict) -> int:
    return v["major"] * 1_000_000 + v["minor"] * 10_000 + v["patch"] * 100 + v["n"]


def main() -> None:
    text = io.open(PKG, encoding="utf-8").read()
    current = re.search(r'"version":\s*"([^"]+)"', text).group(1)
    v = parse(current)

    action = sys.argv[1] if len(sys.argv) > 1 else None
    if action is None:
        print(f"current: {current}  (versionCode {version_code(v)})")
        return

    if action == "tag":
        v["tag"] = v["tag"] or "alpha"
        v["n"] += 1
    elif action == "patch":
        v["patch"] += 1
        v["n"] = 1
    elif action == "minor":
        v["minor"] += 1
        v["patch"] = 0
        v["n"] = 1
    elif action == "stable":
        v["tag"] = None
        v["n"] = 0
    elif action in ("alpha", "beta", "rc"):
        v["tag"] = action
        v["n"] = 1
    else:
        raise SystemExit(f"未知动作：{action}")

    new = render(v)
    text = text.replace(f'"version": "{current}"', f'"version": "{new}"', 1)
    io.open(PKG, "w", encoding="utf-8", newline="\n").write(text)
    print(f"{current} -> {new}  (versionCode {version_code(v)})")


if __name__ == "__main__":
    main()
