import pathlib

from PIL import Image

OUT = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")
DEST = pathlib.Path(r"E:\flutter\open-deepseek\notes")


def checker(size, step=16):
    w, h = size
    img = Image.new("RGB", (w, h), (255, 255, 255))
    px = img.load()
    for y in range(0, h, step):
        for x in range(0, w, step):
            if ((x // step) + (y // step)) % 2 == 0:
                for yy in range(y, min(y + step, h)):
                    for xx in range(x, min(x + step, w)):
                        px[xx, yy] = (204, 204, 204)
    return img


for name in ("welcome", "no-key"):
    art = Image.open(OUT / f"{name}.png").convert("RGBA")
    bg = checker(art.size).convert("RGBA")
    bg.alpha_composite(art)
    bg.convert("RGB").save(DEST / f"preview-{name}.jpg", "JPEG", quality=88)
    print(name, "preview ok")
