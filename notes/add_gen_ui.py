import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()

block = """
/** 生成参数：安全档位与采样直调（Plus 用） */
const GenerationSettings = () => {
  const t = useTranslate()
  const sendSafetyCheck = useSettings((state) => state.sendSafetyCheck)
  const temperature = useSettings((state) => state.temperature)
  const topP = useSettings((state) => state.topP)
  const maxOutputTokens = useSettings((state) => state.maxOutputTokens)

  const numberRow = (
    key: 'temperature' | 'topP' | 'maxOutputTokens',
    label: string,
    hint: string,
    value: number | null,
    placeholder: string
  ) => (
    <SettingCell
      label={label}
      description={hint}
      status={null}
      action={
        <input
          className={styles.input}
          type="number"
          inputMode="decimal"
          step={key === 'topP' ? 0.01 : key === 'temperature' ? 0.05 : 1}
          min={0}
          max={key === 'topP' ? 1 : key === 'temperature' ? 2 : undefined}
          placeholder={placeholder}
          defaultValue={value ?? ''}
          onBlur={(event) => {
            const raw = event.target.value.trim()
            const next = raw === '' ? null : Number(raw)
            setSamplingParam(key, next !== null && Number.isFinite(next) ? next : null)
          }}
        />
      }
    />
  )

  return (
    <div className={styles.group}>
      <div className={styles.groupTitle}>{t('odsGenerationTitle')}</div>
      <SettingCell
        label={t('odsSafetyCheck')}
        description={t('odsSafetyCheckHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={sendSafetyCheck}
            className={clsx(styles.switch, sendSafetyCheck && styles.switchOn)}
            onClick={() => setSendSafetyCheck(!sendSafetyCheck)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />
      {numberRow('temperature', t('odsTemperature'), t('odsTemperatureHint'), temperature, '1')}
      {numberRow('topP', t('odsTopP'), t('odsTopPHint'), topP, '1')}
      {numberRow('maxOutputTokens', t('odsMaxTokens'), t('odsMaxTokensHint'), maxOutputTokens, t('odsParamUnset'))}
    </div>
  )
}
"""

anchor = "const AppearanceSettings = () => {"
assert anchor in t
t = t.replace(anchor, block.strip("\n") + "\n\n" + anchor, 1)

t = t.replace("      <DefaultToggleSettings />", "      <DefaultToggleSettings />\n      <GenerationSettings />", 1)

# import
t = t.replace(
    "  setSearch,",
    "  setSearch,\n  setSendSafetyCheck,\n  setSamplingParam,",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("generation settings ok")
