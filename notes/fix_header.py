import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 顶栏：设置按钮永远靠右，标题缺省时也不挤在左边
p = root / "src/components/session/MobileHeader.module.css"
t = io.open(p, encoding="utf-8").read()
t += """
.settings {
  margin-left: auto;
}
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("css ok")

p = root / "src/components/session/MobileHeader.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """      <IconButton
        size="xl"
        tone="primary"
        icon={<IconSettingsOutline16 />}
        aria-label={t('settings')}
        onClick={() => openSettings('general')}
      />""",
    """      <IconButton
        className={styles.settings}
        size="xl"
        tone="primary"
        icon={<IconSettingsOutline16 />}
        aria-label={t('settings')}
        onClick={() => openSettings('general')}
      />""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("header ok")
