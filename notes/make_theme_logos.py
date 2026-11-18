"""从各主题立绘裁出头部，生成 <id>-logo.webp（128×128，透明底）。"""

import pathlib

from PIL import Image

OUT = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")
NOTES = pathlib.Path(r"E:\flutter\open-deepseek\notes")

# 主题 -> (素材文件, 头部区域相对比例 (left, top, size))
SOURCES = {
    "plain": ("plain-mascot.webp", (0.20, 0.01, 0.60)),
    "ink": ("ink-mascot.webp", (0.18, 0.00, 0.64)),
    "sumi": ("sumi-mascot.webp", (0.20, 0.01, 0.60)),
    "moon": ("moon-mascot.webp", (0.20, 0.00, 0.60)),
    "gyu": ("gyu-mascot.webp", (0.20, 0.00, 0.60)),
    "maid": ("maid-mascot.webp", (0.06, 0.02, 0.88)),
    "tech": ("tech-mascot.webp", (0.02, 0.00, 0.96)),
}

sheet = Image.new("RGB", (128 * len(SOURCES), 128), "white")
for index, (theme, (name, (left, top, size))) in enumerate(SOURCES.items()):
    art = Image.open(OUT / name).convert("RGBA")
    w, h = art.size
    side = int(min(w, h) * size)
    x = int(w * left)
    y = int(h * top + (0 if top > 0 else 0))
    box = (x, y, min(w, x + side), min(h, y + side))
    head = art.crop(box)
    head = head.resize((128, 128), Image.LANCZOS)
    head.save(OUT / f"{theme}-logo.webp", "WEBP", quality=86, method=6)
    print(f"{theme}-logo.webp {(OUT / f'{theme}-logo.webp').stat().st_size // 1024} KB")
    preview = Image.new("RGB", (128, 128), "white")
    preview.paste(head, (0, 0), head)
    sheet.paste(preview, (index * 128, 0))

sheet.save(NOTES / "logo-sheet.jpg", "JPEG", quality=90)
print("sheet ok")
