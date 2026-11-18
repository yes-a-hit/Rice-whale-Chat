import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\settings\LabSettings.tsx")
t = io.open(p, encoding="utf-8").read()
t = t.replace("\nconst LabSettings = () => {", "\nexport const LabSettings = () => {", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("export ok")
