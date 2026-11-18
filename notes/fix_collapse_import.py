import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\settings\ExtSettings.tsx")
t = io.open(p, encoding="utf-8").read()
if "  setCollapseThinking,\n" not in t:
    t = t.replace("  setTtsSystemVoice,", "  setCollapseThinking,\n  setTtsSystemVoice,", 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("import added")
