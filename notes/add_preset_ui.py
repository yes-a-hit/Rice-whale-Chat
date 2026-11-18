import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()

if "ModelPresetSettings" not in t:
    component = '''
/** 模型方案：一套「服务地址 + Key + 模型名」，支持任意 OpenAI 兼容接口 */
const ModelPresetSettings = () => {
  const t = useTranslate()
  const presets = useSettings((state) => state.presets)
  const activePreset = useSettings((state) => state.activePreset)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [draft, setDraft] = useState({ name: '', baseUrl: '', apiKey: '', model: '' })

  const startEdit = (id: string) => {
    const preset = presets.find((item) => item.id === id)
    if (!preset) {
      return
    }
    setDraft({
      name: preset.name,
      baseUrl: preset.baseUrl,
      apiKey: preset.apiKey ?? '',
      model: preset.model,
    })
    setEditingId(id)
  }

  const save = () => {
    if (!editingId) {
      return
    }
    const preset = {
      id: editingId,
      name: draft.name.trim() || draft.model.trim() || '未命名',
      baseUrl: draft.baseUrl.trim(),
      model: draft.model.trim(),
      ...(draft.apiKey.trim() ? { apiKey: draft.apiKey.trim() } : {}),
    }
    savePreset(preset)
    applyPreset(preset.id)
    setEditingId(null)
  }

  const add = () => {
    const id = `preset-${Date.now()}`
    savePreset({ id, name: '新方案', baseUrl: '', model: '' })
    setEditingId(id)
    setDraft({ name: '新方案', baseUrl: '', apiKey: '', model: '' })
  }

  return (
    <div className={styles.group}>
      <div className={styles.groupTitle}>{t('odsPresets')}</div>
      <div className={styles.groupHint}>{t('odsPresetsHint')}</div>
      {presets.map((preset) => (
        <div key={preset.id} className={styles.presetRow}>
          <button
            type="button"
            className={clsx(styles.presetMain, preset.id === activePreset && styles.presetActive)}
            onClick={() => applyPreset(preset.id)}
          >
            <span className={styles.presetName}>{preset.name}</span>
            <span className={styles.presetMeta}>
              {preset.model || '—'} · {preset.baseUrl || t('odsPresetDefaultHost')}
            </span>
          </button>
          <button type="button" className={styles.ghostButton} onClick={() => startEdit(preset.id)}>
            {t('editMessage')}
          </button>
        </div>
      ))}
      {editingId ? (
        <div className={styles.fieldRow}>
          <input
            className={styles.input}
            value={draft.name}
            placeholder={t('odsPresetName')}
            onChange={(event) => setDraft({ ...draft, name: event.target.value })}
          />
          <input
            className={styles.input}
            value={draft.baseUrl}
            placeholder={t('odsPresetBaseUrl')}
            onChange={(event) => setDraft({ ...draft, baseUrl: event.target.value })}
          />
          <input
            className={styles.input}
            value={draft.model}
            placeholder={t('odsPresetModel')}
            onChange={(event) => setDraft({ ...draft, model: event.target.value })}
          />
          <input
            className={styles.input}
            type="password"
            value={draft.apiKey}
            placeholder={t('odsPresetKey')}
            onChange={(event) => setDraft({ ...draft, apiKey: event.target.value })}
          />
          <div className={styles.fieldRow}>
            <button type="button" className={styles.saveButton} onClick={save}>
              {t('confirm')}
            </button>
            <button
              type="button"
              className={styles.ghostButton}
              onClick={() => {
                removePreset(editingId)
                setEditingId(null)
              }}
            >
              {t('delete')}
            </button>
          </div>
        </div>
      ) : null}
      <button type="button" className={styles.ghostButton} onClick={add}>
        {t('odsPresetAdd')}
      </button>
    </div>
  )
}

const ApiBaseUrlSetting = () => {'''
    t = t.replace("const ApiBaseUrlSetting = () => {", component.lstrip("\n"), 1)

    # 渲染顺序：模型方案放在服务地址前面
    t = t.replace(
        "    <ApiBaseUrlSetting />",
        "    <ModelPresetSettings />\n    <ApiBaseUrlSetting />",
        1,
    )

    # 导入
    t = t.replace(
        "  setCollapseThinking,",
        "  applyPreset,\n  removePreset,\n  savePreset,\n  setCollapseThinking,",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("component ok")

# 样式
p = root / "src/components/settings/Ext.module.css"
t = io.open(p, encoding="utf-8").read()
if ".presetRow" not in t:
    t += """
.presetRow {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.presetMain {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 10px;
  border: 1px solid var(--dsw-alias-border-l1);
  border-radius: 10px;
  background: var(--dsw-alias-bg-base);
  text-align: left;
  cursor: pointer;
}

.presetActive {
  border-color: var(--dsw-static-blue-450);
  background: var(--dsw-static-blue-50);
}

.presetName {
  font-size: 14px;
  color: var(--dsw-alias-label-primary);
}

.presetMeta {
  font-size: 12px;
  color: var(--dsw-alias-label-tertiary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("css ok")
