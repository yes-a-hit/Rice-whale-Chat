import io
import pathlib
import re

p = pathlib.Path(r"E:\flutter\open-deepseek\src\app\themes\registry.ts")
t = io.open(p, encoding="utf-8").read()

order = ["plain", "ink", "maid", "tech", "sumi", "moon", "gyu"]
ids = re.findall(r"id: '(\w+)'", t)
assert ids == order, ids

counter = {"n": 0}


def repl(match: "re.Match[str]") -> str:
    index = counter["n"]
    counter["n"] += 1
    return f"logo: '{order[index]}-logo.webp',"


t = re.sub(r"logo: '[^']*',", repl, t)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("replaced", counter["n"])
