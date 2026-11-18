"""重抠女仆立绘：只抠「从四边连通到」的白色，保住白围裙与白领子。"""

import pathlib

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import binary_propagation

ROOT = pathlib.Path(r"E:\flutter\open-deepseek")
OUT = ROOT / "figure" / "out"

src = Image.open(ROOT / "figure" / "logo.png").convert("RGB")
# 原图是 512 方图，人物占中间；先裁掉一圈边缘空白，让主体比例更接近其他立绘
w, h = src.size
src = src.crop((int(w * 0.06), int(h * 0.02), int(w * 0.94), int(h * 0.98)))

rgb = np.asarray(src).astype(np.int16)
top = rgb.max(axis=2)
low = rgb.min(axis=2)
# 更严格的「白」：亮度很高且几乎无色偏
whiteish = (top >= 238) & ((top - low) <= 12)

seeds = np.zeros_like(whiteish)
seeds[0, :] = whiteish[0, :]
seeds[-1, :] = whiteish[-1, :]
seeds[:, 0] = whiteish[:, 0]
seeds[:, -1] = whiteish[:, -1]
paint = binary_propagation(seeds, mask=whiteish)
print("背景占比", round(paint.mean() * 100, 1), "%")

alpha = np.where(paint, 0.0, 1.0).astype(np.float32)
mask = Image.fromarray((alpha * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(0.6))
alpha = np.asarray(mask).astype(np.float32) / 255.0
alpha = np.where(alpha < 0.1, 0.0, alpha)

safe = np.clip(alpha, 1e-3, 1)[..., None]
rgb_f = np.asarray(src).astype(np.float32)
keyed = np.clip((rgb_f - (1 - safe) * 255) / safe, 0, 255).astype(np.uint8)

art = Image.fromarray(keyed, "RGB").convert("RGBA")
art.putalpha(mask.filter(ImageFilter.MinFilter(3)))

target_w = 560
art = art.resize((target_w, round(art.height * target_w / art.width)), Image.LANCZOS)
art = art.quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
art.save(OUT / "maid-mascot.webp", "WEBP", quality=86, method=6)
print("maid-mascot", art.size, (OUT / "maid-mascot.webp").stat().st_size // 1024, "KB")

# 预览：白底 + 棋盘格
full = Image.open(OUT / "maid-mascot.webp").convert("RGBA")
preview = Image.new("RGB", full.size, "white")
step = 16
for yy in range(0, full.height, step):
    for xx in range(0, full.width, step):
        if (xx // step + yy // step) % 2 == 0:
            preview.paste((232, 232, 232), (xx, yy, min(xx + step, full.width), min(yy + step, full.height)))
preview.paste(full, (0, 0), full)
preview.save(ROOT / "notes" / "maid-preview.jpg", "JPEG", quality=88)

# logo 跟着重出
side = int(min(full.size) * 0.8)
head = full.crop((0, 0, side, side)).resize((128, 128), Image.LANCZOS)
head.save(OUT / "maid-logo.webp", "WEBP", quality=86, method=6)
print("maid-logo ok")
