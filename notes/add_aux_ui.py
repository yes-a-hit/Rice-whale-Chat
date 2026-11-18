import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()

block = """
const AuxPromptSetting = () => {
  const t = useTranslate()
  const auxPrompt = useSettings((state) => state.auxPrompt)
  const tailInstruction = useSettings((state) => state.tailInstruction)
  const auxEnabled = useSettings((state) => state.auxEnabled)
  const [auxDraft, setAuxDraft] = useState(auxPrompt)
  const [tailDraft, setTailDraft] = useState(tailInstruction)
  useEffect(() => setAuxDraft(auxPrompt), [auxPrompt])
  useEffect(() => setTailDraft(tailInstruction), [tailInstruction])
  return (
    <>
      <SettingCell
        label={t('odsAuxEnabled')}
        description={t('odsAuxEnabledHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={auxEnabled}
            className={clsx(styles.switch, auxEnabled && styles.switchOn)}
            onClick={() => setAuxEnabled(!auxEnabled)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />
      <SettingCell
        label={t('odsAuxPrompt')}
        description={t('odsAuxPromptHint')}
        status={null}
        stacked
        action={
          <div className={styles.column}>
            <textarea
              className={styles.textarea}
              value={auxDraft}
              rows={7}
              placeholder={DEFAULT_AUX_PROMPT}
              onChange={(event) => setAuxDraft(event.target.value)}
            />
            <div className={styles.buttonRow}>
              <button
                type="button"
                className={styles.saveButton}
                onClick={() => {
                  setAuxPrompt(auxDraft)
                  showToast(t('odsSaved'))
                }}
              >
                {t('odsSave')}
              </button>
              <button
                type="button"
                className={styles.ghostButton}
                onClick={() => {
                  setAuxPrompt(DEFAULT_AUX_PROMPT)
                  setAuxDraft(DEFAULT_AUX_PROMPT)
                  showToast(t('odsSaved'))
                }}
              >
                {t('odsReset')}
              </button>
            </div>
          </div>
        }
      />
      <SettingCell
        label={t('odsTailInstruction')}
        description={t('odsTailInstructionHint')}
        status={null}
        stacked
        action={
          <div className={styles.column}>
            <textarea
              className={styles.textarea}
              value={tailDraft}
              rows={3}
              placeholder={t('odsTailInstructionPlaceholder')}
              onChange={(event) => setTailDraft(event.target.value)}
            />
            <div className={styles.buttonRow}>
              <button
                type="button"
                className={styles.saveButton}
                onClick={() => {
                  setTailInstruction(tailDraft)
                  showToast(t('odsSaved'))
                }}
              >
                {t('odsSave')}
              </button>
            </div>
          </div>
        }
      />
    </>
  )
}

const SystemPromptSetting = () => {"""

t = t.replace("const SystemPromptSetting = () => {", block.lstrip("\n"), 1)
t = t.replace(
    "    <SystemPromptSetting />",
    "    <SystemPromptSetting />\n    <AuxPromptSetting />",
    1,
)
t = t.replace(
    "  setSendSafetyCheck,",
    "  setAuxEnabled,\n  setAuxPrompt,\n  setSendSafetyCheck,\n  setTailInstruction,\n  DEFAULT_AUX_PROMPT,",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("aux ui ok")

# i18n
zh = [
    ("odsAuxEnabled", "启用辅助提示词"),
    ("odsAuxEnabledHint", "只在新会话第一条注入一次，之后随历史滚动；上下文被压缩后会重新注入"),
    ("odsAuxPrompt", "辅助提示词"),
    ("odsAuxPromptHint", "预装的是反鲸八股规则，可改成任意要求；越短越省钱"),
    ("odsTailInstruction", "历史后指令"),
    ("odsTailInstructionHint", "跟在辅助提示词后面，用于强制格式或收尾要求"),
    ("odsTailInstructionPlaceholder", "例如：回答控制在 300 字以内，先给结论"),
]
en = [
    ("odsAuxEnabled", "Inject auxiliary prompt"),
    ("odsAuxEnabledHint", "Injected once at the first turn, then travels with history; re-injected after compression"),
    ("odsAuxPrompt", "Auxiliary prompt"),
    ("odsAuxPromptHint", "Ships with anti-AI-slop rules; shorter costs less"),
    ("odsTailInstruction", "Post-history instruction"),
    ("odsTailInstructionHint", "Appended after the auxiliary prompt, for format or closing constraints"),
    ("odsTailInstructionPlaceholder", "e.g. Keep it under 300 words, lead with the conclusion"),
]
for path, pairs in (("src/i18n/zh.ts", zh), ("src/i18n/en.ts", en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    if pairs[0][0] in t:
        print("skip", path)
        continue
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    t = t.replace(tail, "".join(f"  {k}: '{v}',\n" for k, v in pairs) + tail, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("ok", path)
