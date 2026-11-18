import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 1. moon/gyu 没有立绘文件，去掉 welcome 让它回落默认图
p = root / "src/app/themes/registry.ts"
t = io.open(p, encoding="utf-8").read()
for sid in ("moon", "gyu"):
    t = t.replace(
        f"""    decoration: '{sid}',
    assets: {{
      welcome: '{sid}-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    }},""",
        f"""    decoration: '{sid}',
    // 还没有专属立绘：放 figure/out/{sid}-mascot.webp 后把 welcome 加回来即可
    assets: {{
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    }},""",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("registry fallback ok")

# 2. 奶牛斑点遮罩加深，别让灰块抢视线
p = root / "src/app/themes/themes.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0.93)),
    url('./assets/decor-gyu.webp');""",
    """  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.93), rgba(255, 255, 255, 0.97)),
    url('./assets/decor-gyu.webp');""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("gyu veil ok")
