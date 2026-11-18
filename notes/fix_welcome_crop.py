import io, pathlib

from PIL import Image

root = pathlib.Path(r"E:\flutter\open-deepseek")
fig = root / "figure"
out = fig / "out"

# welcome 原图很横，人物只占中间一小块：裁掉左右空白，让人物更大
src = Image.open(fig / "welcome.jpg").convert("RGB")
w, h = src.size
left = int(w * 0.10)
right = int(w * 0.72)
cropped = src.crop((left, 0, right, h))
print("crop", src.size, "->", cropped.size)

target_w = 760
target_h = round(cropped.height * target_w / cropped.width)
art = cropped.resize((target_w, target_h), Image.LANCZOS)
art = art.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
art.save(out / "welcome.png", "PNG", optimize=True)
print("welcome", art.size, (out / "welcome.png").stat().st_size // 1024, "KB")

# 样式：图再大一点，与输入框之间留点气
p = root / "src/components/session/Welcome.module.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """  .mascot {
    flex-shrink: 0;
    margin: auto 0 12px;
  }""",
    """  .mascot {
    flex-shrink: 0;
    margin: auto 0 18px;
  }""",
    1,
)
t = t.replace(
    """  .mascotImage {
    width: min(330px, 78vw);
    max-height: 46vh;
  }""",
    """  .mascotImage {
    width: min(340px, 82vw);
    max-height: 56vh;
  }""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("css ok")
