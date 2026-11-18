import io, pathlib

from PIL import Image

root = pathlib.Path(r"E:\flutter\open-deepseek")
fig = root / "figure"
out = fig / "out"

# 量化到 256 色，体积减一大半，肉眼看不出差别
for name in ("welcome", "no-key"):
    p = out / f"{name}.png"
    img = Image.open(p).convert("RGB").quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    img.save(p, "PNG", optimize=True)
    print(name, p.stat().st_size // 1024, "KB")

logo = Image.open(out / "logo-128.png").convert("RGB").quantize(colors=256, method=Image.MEDIANCUT)
logo.save(out / "logo-128.png", "PNG", optimize=True)
print("logo", (out / "logo-128.png").stat().st_size // 1024, "KB")

# ---------- 修 Onboarding 缩进 + logo 样式 ----------
p = root / "src/components/onboarding/Onboarding.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """        <img className={styles.logo} src="/media/logo-128.png" alt="" draggable={false} />
      <h1 className={styles.title}>{t('odsOnboardTitle')}</h1>""",
    """        <img className={styles.logo} src="/media/logo-128.png" alt="" draggable={false} />
        <h1 className={styles.title}>{t('odsOnboardTitle')}</h1>""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("onboarding indent ok")

p = root / "src/components/onboarding/Onboarding.module.css"
t = io.open(p, encoding="utf-8").read()
if ".logo" not in t:
    t += """
.logo {
  width: 92px;
  height: 92px;
  margin-bottom: 8px;
  border-radius: 24px;
  object-fit: cover;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  user-select: none;
  -webkit-user-drag: none;
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("onboarding css ok")

# ---------- 侧栏品牌样式 ----------
p = root / "src/components/sider/Sider.module.css"
t = io.open(p, encoding="utf-8").read()
if ".brandLogo" not in t:
    t += """
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.brandLogo {
  width: 26px;
  height: 26px;
  border-radius: 8px;
  flex-shrink: 0;
  object-fit: cover;
  user-select: none;
  -webkit-user-drag: none;
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("sider css ok")
