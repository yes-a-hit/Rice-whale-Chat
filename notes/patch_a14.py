import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- ChatInput: 深度思考始终显示，联网搜索仅 Plus 显示 ----------
p = root / "src/components/chatInput/ChatInput.tsx"
t = io.open(p, encoding="utf-8").read()

old_open = """        <div
          ref={togglesRef}
          className={clsx(styles.toggles, uiMode === 'lite' && styles.togglesHidden)}
        >"""
new_open = """        <div ref={togglesRef} className={styles.toggles}>"""
assert old_open in t
t = t.replace(old_open, new_open, 1)

old_search = """          <Tooltip content={t('deactivatedSearchTooltip')}>
            <button
              type="button"
              className={clsx(styles.toggle, search && styles.selected)}
              aria-label={t('search')}
              aria-pressed={search}
              onClick={() => setSearch(!search)}
            >
              <IconGlobeLanguageOutline14 />
              <span className={styles.toggleLabel}>{t('search')}</span>
            </button>
          </Tooltip>"""
new_search = """          {/* 联网搜索在 Lite 模式隐藏，默认状态由设置里的开关决定 */}
          {uiMode === 'plus' ? (
            <Tooltip content={t('deactivatedSearchTooltip')}>
              <button
                type="button"
                className={clsx(styles.toggle, search && styles.selected)}
                aria-label={t('search')}
                aria-pressed={search}
                onClick={() => setSearch(!search)}
              >
                <IconGlobeLanguageOutline14 />
                <span className={styles.toggleLabel}>{t('search')}</span>
              </button>
            </Tooltip>
          ) : null}"""
assert old_search in t
t = t.replace(old_search, new_search, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ChatInput ok")

# ---------- CSS: 去掉 togglesHidden（不再使用） ----------
p = root / "src/components/chatInput/ChatInput.module.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace("""
/* Lite 模式：隐藏深度思考 / 联网搜索开关，保持界面干净 */
.togglesHidden {
  display: none;
}
""", "")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("css ok")

# ---------- 设置：默认开关（深度思考 / 联网搜索） ----------
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()
if "DefaultToggleSettings" not in t:
    t = t.replace(
        "const AppearanceSettings = () => {",
        """const DefaultToggleSettings = () => {
  const t = useTranslate()
  const thinking = useSettings((state) => state.thinking)
  const search = useSettings((state) => state.search)
  return (
    <>
      <SettingCell
        label={t('odsDefaultThinking')}
        description={t('odsDefaultThinkingHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={thinking}
            className={clsx(styles.switch, thinking && styles.switchOn)}
            onClick={() => setThinking(!thinking)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />
      <SettingCell
        label={t('odsDefaultSearch')}
        description={t('odsDefaultSearchHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={search}
            className={clsx(styles.switch, search && styles.switchOn)}
            onClick={() => setSearch(!search)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />
    </>
  )
}

const AppearanceSettings = () => {""",
        1,
    )
    t = t.replace(
        "  setSkin,\n  setSystemPrompt,",
        "  setSearch,\n  setSkin,\n  setSystemPrompt,\n  setThinking,",
        1,
    )
    t = t.replace(
        """    <ModeSetting />
    <ApiBaseUrlSetting />""",
        """    <ModeSetting />
    <DefaultToggleSettings />
    <ApiBaseUrlSetting />""",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("ExtSettings ok")

# ---------- i18n ----------
zh = [
    ("odsDefaultThinking", "默认开启深度思考"),
    ("odsDefaultThinkingHint", "DeepSeek 的核心能力，建议保持开启"),
    ("odsDefaultSearch", "默认开启联网搜索"),
    ("odsDefaultSearchHint", "开启后每次提问都会检索网页，速度会慢一些"),
]
en = [
    ("odsDefaultThinking", "Thinking on by default"),
    ("odsDefaultThinkingHint", "DeepSeek's core capability; recommended"),
    ("odsDefaultSearch", "Web search on by default"),
    ("odsDefaultSearchHint", "Each question will search the web; replies get slower"),
]

for path, pairs, tail in [
    ("src/i18n/zh.ts", zh, "} as const"),
    ("src/i18n/en.ts", en, "} satisfies Record<keyof typeof zh, string>"),
]:
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    if pairs[0][0] in t:
        print("skip", path)
        continue
    block = "".join(f"  {k}: '{v}',\n" for k, v in pairs)
    t = t.replace(tail, block + tail, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("ok", path)
