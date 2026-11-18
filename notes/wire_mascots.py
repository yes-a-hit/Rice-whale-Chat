import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/app/themes/registry.ts"
t = io.open(p, encoding="utf-8").read()

# 每个主题指向自己的立绘
mapping = {
    "plain": "plain-mascot.webp",
    "sumi": "sumi-mascot.webp",
    "moon": "moon-mascot.webp",
    "gyu": "gyu-mascot.webp",
}
for sid, asset in mapping.items():
    marker = f"    decoration: '{sid}',"
    index = t.find(marker)
    assert index >= 0, sid
    # 在该主题块的 assets 里插入 welcome
    assets_index = t.find("assets: {", index)
    assert assets_index >= 0, sid
    insert_at = assets_index + len("assets: {")
    t = t[:insert_at] + f"\n      welcome: '{asset}'," + t[insert_at:]

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("registry mascots ok")

# 旧的汉服带气泡图不再引用，删掉省体积
old = root / "figure" / "out" / "welcome.webp"
if old.exists():
    old.unlink()
    print("removed welcome.webp")
