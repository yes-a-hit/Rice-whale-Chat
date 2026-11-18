import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\app\themes\themes.css")
t = io.open(p, encoding="utf-8").read()

for theme in ("ink", "maid", "tech", "sumi", "moon", "gyu"):
    old = (
        "  --ods-decor: linear-gradient(var(--ods-veil-1), var(--ods-veil-2)),\n"
        f"    url('./assets/decor-{theme}.webp');"
    )
    new = f"  --ods-image: url('./assets/decor-{theme}.webp');"
    if old in t:
        t = t.replace(old, new, 1)
        print("ok", theme)
    else:
        # 可能还留着旧的固定遮罩写法
        for a in ("0.84", "0.86", "0.88", "0.93"):
            candidate = (
                f"  --ods-decor: linear-gradient(rgba(255, 255, 255, {a}), rgba(255, 255, 255, 0.9{'' if a != '0.9' else ''})),\n"
                f"    url('./assets/decor-{theme}.webp');"
            )
            if candidate in t:
                t = t.replace(candidate, new, 1)
                print("ok(legacy)", theme)
                break
        else:
            print("MISS", theme)

# 兜底：把所有 --ods-decor 行改成 --ods-image
lines = []
for line in t.split("\n"):
    if "--ods-decor:" in line:
        continue
    if line.strip().startswith("url('./assets/decor-") and line.strip().endswith("');"):
        continue
    lines.append(line)
t = "\n".join(lines)

# 清理空行堆积
while "\n\n\n" in t:
    t = t.replace("\n\n\n", "\n\n")

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ods-image count:", t.count("--ods-image"))
