import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- rspack.config.ts：Windows 可用的构建模式判定 ----------
p = root / "rspack.config.ts"
t = io.open(p, encoding="utf-8").read()
old = "const dev = process.env.NODE_ENV !== 'production'"
assert old in t
t = t.replace(
    old,
    "// Windows 下没有 NODE_ENV 前缀语法：构建脚本显式传 --mode production\n"
    "const dev = !process.argv.includes('--mode=production') && process.env.NODE_ENV !== 'production'",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched rspack.config.ts")

# ---------- package.json：跨平台脚本 ----------
p = root / "package.json"
t = io.open(p, encoding="utf-8").read()
old_build = '"build": "rm -rf dist && NODE_ENV=production rspack build -c rspack.config.ts"'
assert old_build in t
t = t.replace(
    old_build,
    '"build": "rspack build -c rspack.config.ts --mode production",\n'
    '    "android:sync": "pnpm build && cap sync android",\n'
    '    "android:apk": "pnpm android:sync && cd android && gradlew.bat assembleDebug",\n'
    '    "android:open": "cap open android"',
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched package.json scripts")
