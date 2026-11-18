import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()

if "export const applyPreset" not in t:
    block = '''
/** 切换模型方案：把方案里的地址/模型/Key 写进当前生效设置 */
export const applyPreset = (id: string) => {
  const state = useSettings.getState()
  const preset = state.presets.find((item) => item.id === id)
  if (!preset) {
    return
  }
  const baseUrl = preset.baseUrl.trim()
  const model = preset.model.trim()
  write(KEYS.activePreset, id)
  if (baseUrl) {
    write(KEYS.apiBaseUrl, baseUrl)
  }
  if (model) {
    write(KEYS.model, model)
  }
  if (preset.apiKey) {
    write(KEYS.apiKey, preset.apiKey)
  }
  useSettings.setState({
    activePreset: id,
    ...(baseUrl ? { apiBaseUrl: baseUrl } : {}),
    ...(model ? { model } : {}),
    ...(preset.apiKey ? { apiKey: preset.apiKey } : {}),
  })
}

const persistPresets = (presets: ProviderPreset[]) => {
  write(KEYS.presets, JSON.stringify(presets))
  useSettings.setState({ presets })
}

/** 新增或更新一个方案 */
export const savePreset = (preset: ProviderPreset) => {
  const list = useSettings.getState().presets
  const exists = list.some((item) => item.id === preset.id)
  persistPresets(exists ? list.map((item) => (item.id === preset.id ? preset : item)) : [...list, preset])
}

export const removePreset = (id: string) => {
  const list = useSettings.getState().presets.filter((item) => item.id !== id)
  persistPresets(list)
}
'''
    anchor = "export const setModel = "
    assert anchor in t
    t = t.replace(anchor, block.lstrip("\n") + "\n" + anchor, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("setters ok")
