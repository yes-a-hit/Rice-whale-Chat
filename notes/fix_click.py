import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\chatInput\ChatInput.tsx")
t = io.open(p, encoding="utf-8").read()
t = t.replace("onClick={openImageDialog}", "onClick={() => openImageDialog()}", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
