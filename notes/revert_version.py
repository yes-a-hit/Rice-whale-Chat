import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\package.json")
t = io.open(p, encoding="utf-8").read()
t = t.replace('"version": "1.0.0-alpha.2"', '"version": "1.0.0-alpha.1"', 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("reverted to 1.0.0-alpha.1")
