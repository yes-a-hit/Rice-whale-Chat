import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

p = root / "src/i18n/zh.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace("odsPresetAdd: '＋ 新增方案',", "odsPresetAdd: '＋ 新增供应商',")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)

p = root / "src/i18n/en.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace("odsPresetAdd: '+ Add preset',", "odsPresetAdd: '+ Add provider',")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("label ok")
