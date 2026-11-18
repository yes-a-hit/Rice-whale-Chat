"""装饰图缩到 640 并保持 webp，作为背景纹理不需要 1024。"""

import pathlib

from PIL import Image

out = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")

for path in sorted(out.glob("decor-*.webp")):
    art = Image.open(path).convert("RGB")
    art = art.resize((640, 640), Image.LANCZOS)
    art.save(path, "WEBP", quality=80, method=6)
    print(f"{path.name:20} {path.stat().st_size // 1024:>4} KB")
