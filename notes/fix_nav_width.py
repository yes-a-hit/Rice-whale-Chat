import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\settings\Settings.module.css")
t = io.open(p, encoding="utf-8").read()

old = """  .navItem {
    flex: 1 0 auto;
    justify-content: center;
    width: auto;
    min-width: 108px;
    margin: 0;
    white-space: nowrap;"""
new = """  .navItem {
    flex: 1 0 auto;
    justify-content: center;
    gap: 6px;
    width: auto;
    min-width: 86px;
    margin: 0;
    padding: 9px 8px;
    white-space: nowrap;"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("nav compacted")
