import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\i18n\en.ts")
t = io.open(p, encoding="utf-8").read()
t = t.replace("DeepSeek's core capability; recommended", "DeepSeek core capability; recommended")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("fixed")
