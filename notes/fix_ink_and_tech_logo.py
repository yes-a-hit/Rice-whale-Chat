import io
import pathlib

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import binary_propagation

ROOT = pathlib.Path(r"E:\flutter\open-deepseek")
OUT = ROOT / "figure" / "out"


def strip_white(art: Image.Image) -> Image.Image:
    rgb = np.asarray(art.convert("RGB")).astype(np.int16)
    top = rgb.max(axis=2)
    low = rgb.min(axis=2)
    whiteish = (top >= 226) & ((top - low) <= 26)
    seeds = np.zeros_like(whiteish)
    seeds[0, :] = whiteish[0, :]
    seeds[-1, :] = whiteish[-1, :]
    seeds[:, 0] = whiteish[:, 0]
    seeds[:, -1] = whiteish[:, -1]
    paint = binary_propagation(seeds, mask=whiteish)
    alpha = np.where(paint, 0.0, 1.0).astype(np.float32)
    mask = Image.fromarray((alpha * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(0.8))
    alpha = np.asarray(mask).astype(np.float32) / 255.0
    alpha = np.where(alpha < 0.12, 0.0, alpha)
    safe = np.clip(alpha, 1e-3, 1)[..., None]
    rgb_f = np.asarray(art.convert("RGB")).astype(np.float32)
    keyed = np.clip((rgb_f - (1 - safe) * 255) / safe, 0, 255).astype(np.uint8)
    result = Image.fromarray(keyed, "RGB").convert("RGBA")
    result.putalpha(mask.filter(ImageFilter.MinFilter(3)))
    return result


# 国风看板娘 = 最初那张汉服 meme（带气泡），裁掉左右空白
src = Image.open(ROOT / "figure" / "welcome.jpg").convert("RGB")
w, h = src.size
crop = src.crop((int(w * 0.10), 0, int(w * 0.72), h))
art = strip_white(crop)
target_w = 760
art = art.resize((target_w, round(art.height * target_w / art.width)), Image.LANCZOS)
art = art.quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
art.save(OUT / "ink-mascot.webp", "WEBP", quality=86, method=6)
print("ink-mascot", art.size, (OUT / "ink-mascot.webp").stat().st_size // 1024, "KB")

# tech logo 重新裁（头部偏右上）
tech = Image.open(OUT / "tech-mascot.webp").convert("RGBA")
tw, th = tech.size
side = int(tw * 0.56)
box = (int(tw * 0.30), int(th * 0.01), int(tw * 0.30) + side, int(th * 0.01) + side)
head = tech.crop(box).resize((128, 128), Image.LANCZOS)
head.save(OUT / "tech-logo.webp", "WEBP", quality=86, method=6)
preview = Image.new("RGB", (128, 128), "white")
preview.paste(head, (0, 0), head)
preview.save(ROOT / "notes" / "tech-logo-preview.jpg", "JPEG", quality=90)
print("tech logo ok")
