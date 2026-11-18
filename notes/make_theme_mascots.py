"""把 moss 出的白底立绘抠成透明 webp，命名 <id>-mascot.webp。"""

import pathlib

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import binary_propagation, label

OUT = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")
N = pathlib.Path(r"E:\flutter\open-deepseek\notes")


def strip_white(art: Image.Image) -> Image.Image:
    rgb = np.asarray(art.convert("RGB")).astype(np.int16)
    top = rgb.max(axis=2)
    low = rgb.min(axis=2)
    whiteish = (top >= 226) & ((top - low) <= 26)

    # 只抠「从四边连通到」的白色，保住衣服里的白眼白
    seeds = np.zeros_like(whiteish)
    seeds[0, :] = whiteish[0, :]
    seeds[-1, :] = whiteish[-1, :]
    seeds[:, 0] = whiteish[:, 0]
    seeds[:, -1] = whiteish[:, -1]
    paint = binary_propagation(seeds, mask=whiteish)

    alpha = np.where(paint, 0.0, 1.0).astype(np.float32)
    mask = Image.fromarray((alpha * 255).astype(np.uint8), "L")
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    alpha = np.asarray(mask).astype(np.float32) / 255.0
    alpha = np.where(alpha < 0.12, 0.0, alpha)

    # 半透明边缘反乘，去掉白边
    safe = np.clip(alpha, 1e-3, 1)[..., None]
    rgb_f = np.asarray(art.convert("RGB")).astype(np.float32)
    keyed = np.clip((rgb_f - (1 - safe) * 255) / safe, 0, 255).astype(np.uint8)

    result = Image.fromarray(keyed, "RGB").convert("RGBA")
    result.putalpha(mask.filter(ImageFilter.MinFilter(3)))
    return result


def main() -> None:
    for path in sorted(OUT.glob("mascot-*.png")):
        theme = path.stem.split("-", 1)[1]
        art = Image.open(path)
        keyed = strip_white(art)
        width = 620
        height = round(keyed.height * width / keyed.width)
        keyed = keyed.resize((width, height), Image.LANCZOS)
        keyed = keyed.quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
        target = OUT / f"{theme}-mascot.webp"
        keyed.save(target, "WEBP", quality=84, method=6)
        print(f"{theme:6} -> {target.name} {target.stat().st_size // 1024} KB")

        preview = Image.new("RGB", (width, height), "white")
        step = 16
        for yy in range(0, height, step):
            for xx in range(0, width, step):
                if (xx // step + yy // step) % 2 == 0:
                    for px in range(xx, min(xx + step, width)):
                        for py in range(yy, min(yy + step, height)):
                            preview.putpixel((px, py), (232, 232, 232))
        preview.paste(Image.open(target).convert("RGBA"), (0, 0), Image.open(target).convert("RGBA"))
        preview.save(N / f"preview-{theme}-mascot.jpg", "JPEG", quality=84)


if __name__ == "__main__":
    main()
