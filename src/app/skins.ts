import { useSettings } from '../services/settings.js'

/** 皮肤：只覆盖主色阶（--dsw-static-blue-*），不改变布局与语义色结构 */
export type SkinId = 'deepseek' | 'ocean' | 'sakura' | 'forest' | 'mono'

export const SKINS: { id: SkinId; labelKey: 'odsSkinDeepseek' | 'odsSkinOcean' | 'odsSkinSakura' | 'odsSkinForest' | 'odsSkinMono' }[] = [
  { id: 'deepseek', labelKey: 'odsSkinDeepseek' },
  { id: 'ocean', labelKey: 'odsSkinOcean' },
  { id: 'sakura', labelKey: 'odsSkinSakura' },
  { id: 'forest', labelKey: 'odsSkinForest' },
  { id: 'mono', labelKey: 'odsSkinMono' },
]

const isSkinId = (value: string): value is SkinId => SKINS.some((skin) => skin.id === value)

/** 同步 html 上的皮肤标记和全局字号；两者都在首屏渲染前调用 */
export const applyAppearance = () => {
  const { skin, fontScale } = useSettings.getState()
  const root = document.documentElement
  const resolved = isSkinId(skin) ? skin : 'deepseek'
  if (resolved === 'deepseek') {
    delete root.dataset.skin
  } else {
    root.dataset.skin = resolved
  }
  // 手机端用 zoom 放大整体界面，比逐个改字号可靠。
  // 同时把倍率写进 --ods-zoom，让 fixed 布局按倍率反算高度，
  // 否则 100dvh 被放大后底部输入框会被裁掉（老登模式「UI 过大遮挡信息」的根因）。
  root.style.setProperty('--ods-zoom', String(fontScale))
  root.style.zoom = fontScale === 1 ? '' : String(fontScale)
}

/** 监听设置变化，自动套用皮肤与字号 */
export const setupAppearance = () => {
  applyAppearance()
  useSettings.subscribe((state, prev) => {
    if (state.skin !== prev.skin || state.fontScale !== prev.fontScale) {
      applyAppearance()
    }
  })
}
