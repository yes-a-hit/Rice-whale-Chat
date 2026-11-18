import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\settings\settingsDialogState.ts")
t = io.open(p, encoding="utf-8").read()

old = """/** 打开状态；`#settings` 便于无交互调试时直接进设置页 */
export const useSettingsDialog = create(() => ({
  open: globalThis.location?.hash === '#settings',
  section: 'general' as SettingsSection,
}))"""
new = """/**
 * 打开状态。`#settings` / `#settings=ext` / `#settings=data` 便于无交互调试时直达某个分组，
 * 正常使用不会带 hash。
 */
const hashSection = (): SettingsSection | null => {
  const hash = globalThis.location?.hash ?? ''
  if (!hash.startsWith('#settings')) {
    return null
  }
  const value = hash.split('=')[1]
  return value === 'ext' || value === 'data' || value === 'general' ? value : 'general'
}

const initialSection = hashSection()

export const useSettingsDialog = create(() => ({
  open: initialSection !== null,
  section: (initialSection ?? 'general') as SettingsSection,
}))"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("hash section ok")
