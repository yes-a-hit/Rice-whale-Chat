import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\services\settings.ts")
t = io.open(p, encoding="utf-8").read()
if "collapseThinking: read(" not in t:
    t = t.replace(
        "  showBalance: read(KEYS.showBalance) !== '0',",
        "  showBalance: read(KEYS.showBalance) !== '0',\n  collapseThinking: read(KEYS.collapseThinking) === 'true',",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("initial value ok")
else:
    print("already")
