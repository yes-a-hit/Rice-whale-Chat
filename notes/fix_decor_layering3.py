import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\app\themes\themes.css")
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    "  /* 月晕边缘偏硬，遮罩再压一点 */\n}",
    "  --ods-image: url('./assets/decor-moon.webp');\n}",
    1,
)
t = t.replace(
    "  /* 黑斑对白底太跳，压到只剩纸纹 */\n}",
    "  --ods-image: url('./assets/decor-gyu.webp');\n}",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ods-image count:", t.count("--ods-image"))
