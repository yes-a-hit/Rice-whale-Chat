import io
import json
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

p = root / "package.json"
t = io.open(p, encoding="utf-8").read()
t = t.replace('"name": "open-deepseek-chat"', '"name": "rice-whale-chat"')
io.open(p, "w", encoding="utf-8", newline="\n").write(t)

p = root / "capacitor.config.json"
t = io.open(p, encoding="utf-8").read()
t = t.replace('"appName": "Open DeepSeek"', '"appName": "Rice Whale Chat"')
io.open(p, "w", encoding="utf-8", newline="\n").write(t)

print(json.loads((root / "capacitor.config.json").read_text(encoding="utf-8"))["appName"])
print(json.loads((root / "package.json").read_text(encoding="utf-8"))["name"])
