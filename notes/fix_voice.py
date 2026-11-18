import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ================= ExtSettings: 语音细调 =================
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()

if "TtsFineTuning" not in t:
    t = t.replace(
        "const VoiceSettings = () => {",
        """const TtsFineTuning = () => {
  const t = useTranslate()
  const engine = useSettings((state) => state.ttsEngine)
  const rate = useSettings((state) => state.ttsRate)
  const systemVoice = useSettings((state) => state.ttsSystemVoice)
  const cloudVoice = useSettings((state) => state.ttsVoice)
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([])

  useEffect(() => {
    if (!('speechSynthesis' in window)) {
      return
    }
    const load = () => {
      const all = window.speechSynthesis.getVoices()
      setVoices(all.filter((voice) => voice.lang.toLowerCase().startsWith('zh')))
    }
    load()
    window.speechSynthesis.addEventListener('voiceschanged', load)
    return () => window.speechSynthesis.removeEventListener('voiceschanged', load)
  }, [])

  return (
    <>
      <SettingCell
        label={t('odsTtsRate')}
        description={t('odsTtsRateHint', { rate: rate.toFixed(1) })}
        status={null}
        stacked
        action={
          <input
            className={styles.range}
            type="range"
            min={0.5}
            max={2}
            step={0.1}
            value={rate}
            aria-label={t('odsTtsRate')}
            onChange={(event) => setTtsRate(Number(event.target.value))}
          />
        }
      />
      {engine === 'system' ? (
        <SettingCell
          label={t('odsTtsSystemVoice')}
          description={t('odsTtsSystemVoiceHint')}
          status={null}
          action={
            <Select<string>
              ariaLabel={t('odsTtsSystemVoice')}
              value={systemVoice}
              options={[
                { value: '', label: t('odsTtsSystemVoiceAuto') },
                ...voices.map((voice) => ({ value: voice.name, label: voice.name })),
              ]}
              onChange={(value) => setTtsSystemVoice(value)}
            />
          }
        />
      ) : null}
      {engine === 'cloud' ? (
        <SettingCell
          label={t('odsTtsCloudVoice')}
          description={t('odsTtsCloudVoiceHint')}
          status={null}
          action={
            <Select<string>
              ariaLabel={t('odsTtsCloudVoice')}
              value={cloudVoice}
              options={[
                { value: 'stella', label: t('ttsVoiceStella') },
                { value: 'tide', label: t('ttsVoiceTide') },
              ]}
              onChange={(value) => setTtsVoice(value === 'tide' ? 'tide' : 'stella')}
            />
          }
        />
      ) : null}
    </>
  )
}

const VoiceSettings = () => {""",
        1,
    )
    # 插到引擎选择之后
    t = t.replace(
        """      <SettingCell
        label={t('odsAsrEngine')}""",
        """      <TtsFineTuning />
      <SettingCell
        label={t('odsAsrEngine')}""",
        1,
    )
    # 补 import
    t = t.replace(
        "  setTtsEngine,",
        "  setTtsEngine,\n  setTtsRate,\n  setTtsSystemVoice,\n  setTtsVoice,",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("ExtSettings ok")

# ================= 角色卡与系统提示词分离 =================
p = root / "src/components/settings/CharacterCardSetting.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { setSystemPrompt, useSettings } from '../../services/settings.js'",
    "import { setCharacterPrompt, useSettings } from '../../services/settings.js'",
    1,
)
t = t.replace(
    "  const systemPrompt = useSettings((state) => state.systemPrompt)",
    "  const characterPrompt = useSettings((state) => state.characterPrompt)\n"
    "  const characterName = useSettings((state) => state.characterName)",
    1,
)
t = t.replace(
    "  const current = systemPrompt.trim().split('\\n')[0]?.slice(0, 80) ?? ''",
    "  const current = characterName || characterPrompt.trim().split('\\n')[0]?.slice(0, 40) || ''",
    1,
)
t = t.replace(
    "      setSystemPrompt(buildCardSystemPrompt(card))",
    "      setCharacterPrompt(buildCardSystemPrompt(card), card.name)",
    1,
)
t = t.replace(
    "          {systemPrompt.trim() ? (\n            <button type=\"button\" className={styles.ghostButton} onClick={() => setSystemPrompt('')}>",
    "          {characterPrompt.trim() ? (\n            <button type=\"button\" className={styles.ghostButton} onClick={() => setCharacterPrompt('', '')}>",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("CharacterCardSetting ok")

# ================= 语速滑块样式 =================
p = root / "src/components/settings/Ext.module.css"
t = io.open(p, encoding="utf-8").read()
if ".range" not in t:
    t += """
.range {
  flex: 1;
  width: 100%;
  accent-color: var(--dsw-alias-brand-primary);
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("css range ok")
