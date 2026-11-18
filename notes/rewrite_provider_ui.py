import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()

start = t.find("/** 模型方案：一套「服务地址 + Key + 模型名」，支持任意 OpenAI 兼容接口 */")
end = t.find("const ApiBaseUrlSetting = () => {")
assert start >= 0 and end > start

new_component = '''/**
 * 供应商 + 模型：一个供应商是一套「地址 + Key」，下面挂多个模型。
 * 选中供应商后，再从中挑一个模型作为当前模型。
 */
const ModelPresetSettings = () => {
  const t = useTranslate()
  const providers = useSettings((state) => state.providers)
  const activeProvider = useSettings((state) => state.activeProvider)
  const model = useSettings((state) => state.model)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [draft, setDraft] = useState({ name: '', baseUrl: '', apiKey: '', models: '' })

  const startEdit = (id: string) => {
    const provider = providers.find((item) => item.id === id)
    if (!provider) {
      return
    }
    setDraft({
      name: provider.name,
      baseUrl: provider.baseUrl,
      apiKey: provider.apiKey ?? '',
      models: provider.models.join('\\n'),
    })
    setEditingId(id)
  }

  const save = () => {
    if (!editingId) {
      return
    }
    const models = draft.models
      .split(/[\\n,]/)
      .map((item) => item.trim())
      .filter(Boolean)
    const provider = {
      id: editingId,
      name: draft.name.trim() || draft.baseUrl.trim() || '未命名供应商',
      baseUrl: draft.baseUrl.trim(),
      models,
      ...(draft.apiKey.trim() ? { apiKey: draft.apiKey.trim() } : {}),
    }
    saveProvider(provider)
    applyProvider(provider.id)
    setEditingId(null)
  }

  const add = () => {
    const id = `provider-${Date.now()}`
    saveProvider({ id, name: '新供应商', baseUrl: '', models: [] })
    setEditingId(id)
    setDraft({ name: '新供应商', baseUrl: '', apiKey: '', models: '' })
  }

  return (
    <div className={styles.group}>
      <div className={styles.groupTitle}>{t('odsProviders')}</div>
      <div className={styles.groupHint}>{t('odsProvidersHint')}</div>
      {providers.map((provider) => (
        <div key={provider.id} className={styles.presetBlock}>
          <div className={styles.presetRow}>
            <button
              type="button"
              className={clsx(styles.presetMain, provider.id === activeProvider && styles.presetActive)}
              onClick={() => applyProvider(provider.id)}
            >
              <span className={styles.presetName}>{provider.name}</span>
              <span className={styles.presetMeta}>
                {provider.baseUrl || t('odsPresetDefaultHost')} · {provider.models.length} 个模型
              </span>
            </button>
            <button type="button" className={styles.ghostButton} onClick={() => startEdit(provider.id)}>
              {t('odsPresetEdit')}
            </button>
          </div>
          {provider.id === activeProvider && provider.models.length > 0 ? (
            <div className={styles.modelChips}>
              {provider.models.map((item) => (
                <button
                  key={item}
                  type="button"
                  className={clsx(styles.modelChip, item === model && styles.modelChipActive)}
                  onClick={() => setModel(item)}
                >
                  {item}
                </button>
              ))}
            </div>
          ) : null}
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
            type="password"
            value={draft.apiKey}
            placeholder={t('odsPresetKey')}
            onChange={(event) => setDraft({ ...draft, apiKey: event.target.value })}
          />
          <textarea
            className={styles.textarea}
            value={draft.models}
            rows={3}
            placeholder={t('odsProviderModels')}
            onChange={(event) => setDraft({ ...draft, models: event.target.value })}
          />
          <div className={styles.fieldRow}>
            <button type="button" className={styles.saveButton} onClick={save}>
              {t('confirm')}
            </button>
            <button
              type="button"
              className={styles.ghostButton}
              onClick={() => {
                removeProvider(editingId)
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

'''
t = t[:start] + new_component + t[end:]

t = t.replace(
    "  applyPreset,\n  removePreset,\n  savePreset,\n  setCollapseThinking,",
    "  applyProvider,\n  removeProvider,\n  saveProvider,\n  setCollapseThinking,",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("component ok")
