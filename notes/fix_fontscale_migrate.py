import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\services\settings.ts")
t = io.open(p, encoding="utf-8").read()
old = """const initialFontScale = (): number => {
  const saved = Number(read(KEYS.fontScale))
  return Number.isFinite(saved) && saved >= 0.8 && saved <= 2 ? saved : 1
}"""
new = """const initialFontScale = (): number => {
  const saved = Number(read(KEYS.fontScale))
  if (!Number.isFinite(saved) || saved < 0.8 || saved > 2) {
    return 1
  }
  // 1.15 是老版本给 Lite 的默认值，会顶到屏幕边缘，统一收敛到 1.08
  return saved === 1.15 ? 1.08 : saved
}"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("font scale migration ok")
