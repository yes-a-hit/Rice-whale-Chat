import { create } from 'zustand'
import { useSettings } from '../../services/settings.js'

/** 设置弹窗的分组：通用设置 / 扩展 / 数据管理 */
export type SettingsSection = 'general' | 'ext' | 'usage' | 'data'

/** 设置弹窗：侧边栏底部、没有 API Key 时的操作与 401 提示都可以打开；section 为打开时选中的分组 */
/**
 * 打开状态。`#settings` / `#settings=ext` / `#settings=data` 便于无交互调试时直达某个分组，
 * 正常使用不会带 hash。
 */
const hashSection = (): SettingsSection | null => {
  const hash = globalThis.location?.hash ?? ''
  if (!hash.startsWith('#settings')) {
    return null
  }
  const value = hash.split('=')[1]
  return value === 'ext' || value === 'data' || value === 'usage' || value === 'general'
    ? value
    : 'general'
}

const initialSection = hashSection()

export const useSettingsDialog = create(() => ({
  open: initialSection !== null,
  section: (initialSection ?? 'general') as SettingsSection,
}))

export const openSettings = (section: SettingsSection) =>
  useSettingsDialog.setState({ open: true, section })

export const closeSettings = () => useSettingsDialog.setState({ open: false })

/**
 * 是否已有 API Key。
 * 没有 Key 时不再强行弹设置——欢迎页会用角色图 + 「去设置」按钮引导，
 * 长辈第一次打开看到的是图，不是一屏表单。
 */
export const ensureApiKey = () => Boolean(useSettings.getState().apiKey)
