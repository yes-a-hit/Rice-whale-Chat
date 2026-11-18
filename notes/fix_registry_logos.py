import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 1. 修 registry：按主题顺序逐个替换 logo
p = root / "src/app/themes/registry.ts"
t = io.open(p, encoding="utf-8").read()
for theme in ("plain", "ink", "maid", "tech", "sumi", "moon", "gyu"):
    id_index = t.find(f"id: '{theme}',")
    assert id_index >= 0, theme
    logo_index = t.find("logo: 'logo-128.webp',", id_index)
    if logo_index >= 0:
        t = t[:logo_index] + f"logo: '{theme}-logo.webp'," + t[logo_index + len("logo: 'logo-128.webp',"):]
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("logos:", t.count("-logo.webp"), "张")

# 2. 检查 applyAppearance 是否写 --ods-image
p = root / "src/app/skins.ts"
t = io.open(p, encoding="utf-8").read()
print("has ods-image:", "--ods-image" in t)
