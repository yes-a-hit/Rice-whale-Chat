import io
import pathlib
import shutil

root = pathlib.Path(r"E:\flutter\open-deepseek")

p = root / "src/app/themes/registry.ts"
t = io.open(p, encoding="utf-8").read()

# plain：补上自己的立绘
t = t.replace(
    """    // 最简 = 原版观感：不挂主题立绘，用通用那张
    assets: {
      hungry: 'hungry.webp',""",
    """    assets: {
      welcome: 'plain-mascot.webp',
      hungry: 'hungry.webp',""",
    1,
)
# sumi：换成水墨立绘
t = t.replace(
    """    assets: {
      welcome: 'welcome.webp',
      hungry: 'hungry.webp',""",
    """    assets: {
      welcome: 'sumi-mascot.webp',
      hungry: 'hungry.webp',""",
    1,
)
# gyu：补上奶牛立绘
t = t.replace(
    """    assets: {
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
    match: {
      models: ['glm', 'chatglm', 'zhipu'],""",
    """    assets: {
      welcome: 'gyu-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
    match: {
      models: ['glm', 'chatglm', 'zhipu'],""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("registry updated")

# 原始大图不该进 assets：挪到 notes/src-art
art_dir = root / "notes" / "src-art"
art_dir.mkdir(exist_ok=True)
for path in sorted((root / "figure" / "out").glob("mascot-*.png")):
    shutil.move(str(path), str(art_dir / path.name))
    print("moved", path.name)

old = root / "figure" / "out" / "welcome.webp"
if old.exists():
    old.unlink()
    print("removed welcome.webp")
