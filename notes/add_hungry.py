import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\strip_white.py")
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    """build("welcome", 760, (0.10, 0.72))
build("no-key", 800)""",
    """build("welcome", 760, (0.10, 0.72))
build("no-key", 800)
build("hungry", 800)""",
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("script updated")
