import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. Welcome 加 DOM 气泡 ----------
p = root / "src/components/session/Welcome.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """        <div className={styles.mascot}>
          <img""",
    """        <div className={styles.mascot}>
          {hasApiKey ? <div className={styles.bubble}>{t('odsWelcomeBubble')}</div> : null}
          <img""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("welcome bubble ok")

# ---------- 2. 气泡样式 ----------
p = root / "src/components/session/Welcome.module.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    ".mascot {",
    """.bubble {
  position: absolute;
  left: 0;
  top: 6%;
  z-index: 1;
  max-width: 44%;
  padding: 9px 13px;
  border: 1.5px solid var(--dsw-alias-label-primary);
  border-radius: 16px;
  background: var(--dsw-alias-bg-base);
  color: var(--dsw-alias-label-primary);
  font-size: 13.5px;
  line-height: 1.45;
  white-space: pre-line;
  pointer-events: none;
}

.bubble::after {
  content: '';
  position: absolute;
  right: -9px;
  top: 52%;
  width: 10px;
  height: 10px;
  border-right: 1.5px solid var(--dsw-alias-label-primary);
  border-bottom: 1.5px solid var(--dsw-alias-label-primary);
  background: var(--dsw-alias-bg-base);
  transform: rotate(-45deg);
}

.mascot {""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("bubble css ok")

# ---------- 3. registry：汉服图归到国风，plain 暂不指定立绘 ----------
p = root / "src/app/themes/registry.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """    decoration: 'none',
    assets: {
      welcome: 'welcome.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },""",
    """    decoration: 'none',
    // 最简 = 原版观感：不挂主题立绘，用通用那张
    assets: {
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },""",
    1,
)
t = t.replace(
    """    decoration: 'ink',
    assets: {
      welcome: 'welcome.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },""",
    """    decoration: 'ink',
    // 汉服鲸鱼女仆是国风的主角
    assets: {
      welcome: 'ink-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("registry ok")

# ---------- 4. i18n ----------
pairs_zh = [("odsWelcomeBubble", "欢迎回来，\\n想从哪里开始")]
pairs_en = [("odsWelcomeBubble", "Welcome back.\\nWhere should we start?")]
for path, pairs in (("src/i18n/zh.ts", pairs_zh), ("src/i18n/en.ts", pairs_en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    if pairs[0][0] in t:
        continue
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    t = t.replace(tail, "".join(f"  {k}: '{v}',\n" for k, v in pairs) + tail, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("i18n ok", path)
