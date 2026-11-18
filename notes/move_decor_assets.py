import io
import pathlib
import shutil

root = pathlib.Path(r"E:\flutter\open-deepseek")
src_dir = root / "figure" / "out"
dst_dir = root / "src" / "app" / "themes" / "assets"
dst_dir.mkdir(parents=True, exist_ok=True)

for path in sorted(src_dir.glob("decor-*.webp")):
    target = dst_dir / path.name
    shutil.copy2(path, target)
    path.unlink()
    print("moved", path.name, target.stat().st_size // 1024, "KB")

# CSS 里改成相对路径，交给打包器处理并加 hash
css = root / "src/app/themes/themes.css"
t = io.open(css, encoding="utf-8").read()
for name in ("ink", "maid", "tech", "sumi", "moon", "gyu"):
    t = t.replace(f"url('/media/decor-{name}.webp')", f"url('./assets/decor-{name}.webp')")
io.open(css, "w", encoding="utf-8", newline="\n").write(t)
print("css paths ok")
