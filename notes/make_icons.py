import io
import pathlib

from PIL import Image, ImageDraw

root = pathlib.Path(r"E:\flutter\open-deepseek")
fig = root / "figure"
out = fig / "out"
out.mkdir(exist_ok=True)
res = root / "android/app/src/main/res"

logo = Image.open(fig / "logo.png").convert("RGB")

# ---------- 1. 应用内 web 图片：welcome / no-key 压到 720 宽 ----------
for name in ("welcome", "no-key"):
    src = Image.open(fig / f"{name}.jpg").convert("RGB")
    width = 820
    height = round(src.height * width / src.width)
    thumb = src.resize((width, height), Image.LANCZOS)
    thumb.save(out / f"{name}.webp", "WEBP", quality=82, method=6)
    print(name, thumb.size, (out / f"{name}.webp").stat().st_size // 1024, "KB")

# ---------- 2. Android 普通图标 ----------
LAUNCHER = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
# adaptive icon 前景层：内容只占中间 ~66%，四周留白避免被圆形遮罩切掉
FOREGROUND = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}
BG = (255, 255, 255)


def make_square(size: int, content_ratio: float, circular: bool) -> Image.Image:
    canvas = Image.new("RGB", (size, size), BG)
    inner = max(1, int(size * content_ratio))
    art = logo.resize((inner, inner), Image.LANCZOS)
    offset = (size - inner) // 2
    canvas.paste(art, (offset, offset))
    if circular:
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
        rounded = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        rounded.paste(canvas, (0, 0), mask)
        return rounded
    return canvas


for dpi, size in LAUNCHER.items():
    folder = res / f"mipmap-{dpi}"
    folder.mkdir(parents=True, exist_ok=True)
    make_square(size, 0.92, False).save(folder / "ic_launcher.png")
    make_square(size, 0.92, True).save(folder / "ic_launcher_round.png")
    print("launcher", dpi, size)

for dpi, size in FOREGROUND.items():
    folder = res / f"mipmap-{dpi}"
    folder.mkdir(parents=True, exist_ok=True)
    # 前景层保持不透明白底 + 居中缩放，掩罩由系统负责
    make_square(size, 0.66, False).save(folder / "ic_launcher_foreground.png")
    print("foreground", dpi, size)

# ---------- 3. 启动画面（沿用 Capacitor 的尺寸，用 logo 居中） ----------
SPLASH = {
    "drawable": (480, 480),
    "drawable-land-mdpi": (480, 320),
    "drawable-land-hdpi": (800, 480),
    "drawable-land-xhdpi": (1280, 720),
    "drawable-land-xxhdpi": (1600, 960),
    "drawable-land-xxxhdpi": (1920, 1280),
    "drawable-port-mdpi": (320, 480),
    "drawable-port-hdpi": (480, 800),
    "drawable-port-xhdpi": (720, 1280),
    "drawable-port-xxhdpi": (960, 1600),
    "drawable-port-xxxhdpi": (1280, 1920),
}
for folder_name, (w, h) in SPLASH.items():
    canvas = Image.new("RGB", (w, h), BG)
    side = int(min(w, h) * 0.42)
    art = logo.resize((side, side), Image.LANCZOS)
    canvas.paste(art, ((w - side) // 2, (h - side) // 2))
    folder = res / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    canvas.save(folder / "splash.png")
print("splash done")
