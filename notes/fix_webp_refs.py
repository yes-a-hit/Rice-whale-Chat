import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek\src")
mapping = {
    "/media/logo-128.png": "/media/logo-128.webp",
    "/media/welcome.png": "/media/welcome.webp",
    "/media/hungry.png": "/media/hungry.webp",
    "/media/wait.png": "/media/wait.webp",
}

for path in root.rglob("*.tsx"):
    t = io.open(path, encoding="utf-8").read()
    original = t
    for old, new in mapping.items():
        t = t.replace(old, new)
    if t != original:
        io.open(path, "w", encoding="utf-8", newline="\n").write(t)
        print("updated", path.relative_to(root.parent))
