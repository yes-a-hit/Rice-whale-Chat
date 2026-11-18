import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
out = root / "figure" / "out"
notes = root / "notes"

# 预览图不放进 assets 目录，避免被 copy 进 APK
for p in out.glob("preview-*.jpg"):
    p.unlink()
    print("removed", p.name)

p = root / "notes/preview_alpha.py"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    'OUT = pathlib.Path(r"E:\\flutter\\open-deepseek\\figure\\out")',
    'OUT = pathlib.Path(r"E:\\flutter\\open-deepseek\\figure\\out")\nDEST = pathlib.Path(r"E:\\flutter\\open-deepseek\\notes")',
)
t = t.replace('bg.convert("RGB").save(OUT / f"preview-{name}.jpg"', 'bg.convert("RGB").save(DEST / f"preview-{name}.jpg"')
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("preview output moved to notes/")

# 透明图不需要圆角与白底
p = root / "src/components/session/Welcome.module.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """  object-fit: contain;
  user-select: none;
  -webkit-user-drag: none;
}""",
    """  object-fit: contain;
  /* 素材已去白底，透明区域直接透出页面背景，不再需要圆角遮罩 */
  background: none;
  user-select: none;
  -webkit-user-drag: none;
}""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("welcome css ok")
