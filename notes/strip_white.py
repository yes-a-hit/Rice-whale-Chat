"""
从原始 JPG 生成透明底梗图（可重复执行，输入永远是 figure/*.jpg）。

只把「与画布边缘连通的白色」变透明：人物白衣服、白眼白、对话气泡内部保持原样。
输出：welcome.png / wait.png（原 no-key）/ hungry.png，均为 256 色带 alpha 的 PNG。
"""

import pathlib

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

FIG = pathlib.Path(r"E:\flutter\open-deepseek\figure")
OUT = FIG / "out"


def cut_white(img: Image.Image, lum_min: int = 226, sat_max: int = 26) -> Image.Image:
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    lum = arr.mean(axis=2)
    sat = arr.max(axis=2) - arr.min(axis=2)
    white = (lum >= lum_min) & (sat <= sat_max)

    seed = np.zeros_like(white)
    seed[0, :] = white[0, :]
    seed[-1, :] = white[-1, :]
    seed[:, 0] = white[:, 0]
    seed[:, -1] = white[:, -1]
    outside = ndimage.binary_propagation(seed, mask=white)

    alpha = np.where(outside, 0.0, 1.0)
    soft = ndimage.gaussian_filter(alpha, sigma=0.8)
    alpha = np.clip((soft - 0.35) / 0.3, 0.0, 1.0)

    a = alpha[..., None]
    safe = np.where(a < 0.05, 1.0, a)
    rgb = np.clip(np.where(a < 0.97, (arr - (1.0 - a) * 255.0) / safe, arr), 0, 255)

    out = Image.fromarray(np.dstack([rgb, alpha * 255.0]).astype(np.uint8), "RGBA")
    out.putalpha(out.split()[3].filter(ImageFilter.MinFilter(3)))
    return out


def build(src_name: str, out_name: str, width: int, crop: tuple[float, float] | None = None) -> None:
    src = Image.open(FIG / f"{src_name}.jpg").convert("RGB")
    if crop:
        w, h = src.size
        src = src.crop((int(w * crop[0]), 0, int(w * crop[1]), h))
    height = round(src.height * width / src.width)
    src = src.resize((width, height), Image.LANCZOS)

    art = cut_white(src).quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)

    path = OUT / f"{out_name}.png"
    art.save(path, "PNG", optimize=True)

    alpha = np.asarray(art.convert("RGBA"))[..., 3]
    print(
        f"{out_name}.png  {art.size[0]}x{art.size[1]}  "
        f"透明 {int((alpha == 0).sum()) * 100 // alpha.size}%  "
        f"{path.stat().st_size // 1024} KB"
    )


build("welcome", "welcome", 760, (0.10, 0.72))
build("no-key", "wait", 800)
build("hungry", "hungry", 800)
