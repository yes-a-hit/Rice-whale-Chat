import io, pathlib

from PIL import Image

root = pathlib.Path(r"E:\flutter\open-deepseek")
fig = root / "figure"
out = fig / "out"

# 统一用 PNG：Android WebView 对 png 的 MIME 处理最稳
for name in ("welcome", "no-key"):
    src = Image.open(fig / f"{name}.jpg").convert("RGB")
    width = 800
    height = round(src.height * width / src.width)
    src.resize((width, height), Image.LANCZOS).save(out / f"{name}.png", "PNG", optimize=True)
    print(name, (out / f"{name}.png").stat().st_size // 1024, "KB")

logo = Image.open(fig / "logo.png").convert("RGB")
logo.resize((128, 128), Image.LANCZOS).save(out / "logo-128.png", "PNG", optimize=True)
print("logo ok")

# 清理 webp 版本，避免 dist 里两份
for old in ("welcome.webp", "no-key.webp", "logo-128.webp"):
    p = out / old
    if p.exists():
        p.unlink()

# 引用改成 png
for path in ("src/components/session/Welcome.tsx", "src/components/sider/Sider.tsx"):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    t = t.replace(".webp", ".png")
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("updated", path)

# 引导页加 logo
p = root / "src/components/onboarding/Onboarding.tsx"
t = io.open(p, encoding="utf-8").read()
if "onboardingLogo" not in t:
    old = """      <h1 className={styles.title}>"""
    new = """      <img className={styles.logo} src="/media/logo-128.png" alt="" draggable={false} />
      <h1 className={styles.title}>"""
    if old in t:
        t = t.replace(old, new, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("onboarding logo ok")
    else:
        print("onboarding anchor missing")
