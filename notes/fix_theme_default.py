import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\services\settings.ts")
t = io.open(p, encoding="utf-8").read()

old = "  skin: read(KEYS.skin) ?? DEFAULT_SKIN,"
assert old in t
t = t.replace(old, "  skin: read(KEYS.skin) ?? DEFAULT_SKIN,\n  themeAuto: read(KEYS.themeAuto) === 'true',", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("themeAuto default ok")
