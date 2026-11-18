import pathlib

from PIL import Image

OUT = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")

for name in ("welcome", "no-key"):
    p = OUT / f"{name}.png"
    art = Image.open(p).convert("RGBA")
    before = p.stat().st_size // 1024

    # FASTOCTREE 支持带 alpha 的调色板量化，透明区保持全透明
    quant = art.quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
    quant.save(p, "PNG", optimize=True)
    print(f"{name}.png  {before} KB -> {p.stat().st_size // 1024} KB")
