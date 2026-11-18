import io
import pathlib

from PIL import Image, ImageDraw, ImageFilter

root = pathlib.Path(r"E:\flutter\open-deepseek\figure")
out = root / "out"
notes = pathlib.Path(r"E:\flutter\open-deepseek\notes")

src = Image.open(root / "tech-plus.jpg").convert("RGB")
w, h = src.size

# 上半身（头到腰），避开底部的地面光斑
box = (int(w * 0.315), int(h * 0.02), int(w * 0.545), int(h * 0.46))
crop = src.crop(box)
print("crop", crop.size)

pixels = crop.convert("RGBA")
data = pixels.load()
cw, ch = pixels.size
for y in range(ch):
    for x in range(cw):
        r, g, b, _a = data[x, y]
        top = max(r, g, b)
        if top < 78:
            alpha = 0 if top < 55 else int((top - 55) / 23 * 255)
            data[x, y] = (r, g, b, alpha)

mask = pixels.split()[3].filter(ImageFilter.GaussianBlur(0.6))
pixels.putalpha(mask)

target_w = 560
target_h = round(pixels.height * target_w / pixels.width)
art = pixels.resize((target_w, target_h), Image.LANCZOS)
art.save(out / "tech-mascot.png", "PNG", optimize=True)
print("tech-mascot", art.size, (out / "tech-mascot.png").stat().st_size // 1024, "KB")

preview = Image.new("RGB", art.size, "white")
draw = ImageDraw.Draw(preview)
step = 16
for yy in range(0, art.height, step):
    for xx in range(0, art.width, step):
        if (xx // step + yy // step) % 2 == 0:
            draw.rectangle([xx, yy, xx + step - 1, yy + step - 1], fill=(232, 232, 232))
preview.paste(art, (0, 0), art)
preview.save(notes / "preview-tech-mascot.jpg", "JPEG", quality=86)
print("preview ok")
