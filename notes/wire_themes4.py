import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. .frame 接受主题装饰 ----------
p = root / "src/app/App.module.css"
t = io.open(p, encoding="utf-8").read()
old = """  overflow: hidden;
  background-color: var(--dsw-alias-bg-base);
}"""
new = """  overflow: hidden;
  background-color: var(--dsw-alias-bg-base);
  /* 主题装饰：由 themes.css 里的 --ods-decor 提供，缺省无 */
  background-image: var(--ods-decor, none);
  background-attachment: local;
}"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("frame decor ok")

# ---------- 2. 缺素材的主题回落到默认图 ----------
p = root / "src/app/themes/registry.ts"
t = io.open(p, encoding="utf-8").read()
for sid in ("moon", "gyu"):
    t = t.replace(
        f"""    id: '{sid}',
    nameKey: 'odsTheme{sid.capitalize()}',""",
        f"""    id: '{sid}',
    nameKey: 'odsTheme{sid.capitalize()}',""",
        1,
    )
t = t.replace(
    """    decoration: 'moon',
    assets: {
      welcome: 'moon-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },""",
    """    decoration: 'moon',
    // 素材槽留空即回落默认立绘；放 figure/out/moon-mascot.webp 就会自动用上
    assets: {
      welcome: 'moon-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("registry ok")
