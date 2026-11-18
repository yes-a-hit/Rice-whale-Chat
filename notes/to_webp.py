import pathlib

from PIL import Image

out = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")

for png in sorted(out.glob("*.png")):
    img = Image.open(png)
    target = png.with_suffix(".webp")
    # 有 alpha 的保 alpha，质量 82 肉眼无差，体积大约降到一半以下
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        img.save(target, "WEBP", quality=82, method=6)
    else:
        img.convert("RGB").save(target, "WEBP", quality=82, method=6)
    before = png.stat().st_size // 1024
    after = target.stat().st_size // 1024
    print(f"{png.name:22} {before:5} KB -> {target.name:22} {after:5} KB")
    png.unlink()
