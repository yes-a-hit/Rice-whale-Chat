"""女仆主题素材：logo.png 是女仆装半身像，去白底后直接当立绘。"""

import pathlib

from PIL import Image, ImageFilter

root = pathlib.Path(r"E:\flutter\open-deepseek\figure")
out = root / "out"

src = Image.open(root / "logo.png").convert("RGBA")
w, h = src.size

# 只去掉接近纯白的背景，保留衣服与皮肤
data = src.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = data[x, y]
        if a == 0:
            continue
        if r > 236 and g > 236 and b > 236:
            data[x, y] = (r, g, b, 0)

alpha = src.split()[3].filter(ImageFilter.GaussianBlur(0.5))
src.putalpha(alpha)

target_w = 520
target_h = round(src.height * target_w / src.width)
art = src.resize((target_w, target_h), Image.LANCZOS)
art.save(out / "maid-mascot.webp", "WEBP", quality=84, method=6)
print("maid-mascot", art.size, (out / "maid-mascot.webp").stat().st_size // 1024, "KB")
