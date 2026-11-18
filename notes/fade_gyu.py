"""把奶牛主题的装饰底图调淡，避免黑斑在浅色模式下变成突兀的灰块。"""

import pathlib

from PIL import Image

out = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")
src = Image.open(out / "decor-gyu.webp").convert("RGB")

# 向白色靠 55%，保留纹理但压低对比
faded = Image.blend(src, Image.new("RGB", src.size, "white"), 0.55)
faded.save(out / "decor-gyu.webp", "WEBP", quality=84, method=6)
print("decor-gyu", (out / "decor-gyu.webp").stat().st_size // 1024, "KB")

# 同步到源码目录，保持两处一致
(src_dir := pathlib.Path(r"E:\flutter\open-deepseek\src\app\themes\assets") / "decor-gyu.webp").write_bytes(
    (out / "decor-gyu.webp").read_bytes()
)
print("synced")
