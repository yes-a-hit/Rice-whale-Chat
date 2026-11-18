import { useSettings } from '../services/settings.js'
import { matchTheme } from './themes/types.js'
import { DEFAULT_THEME, isThemeId, THEMES, themeById } from './themes/registry.js'
import type { ThemeId } from './themes/types.js'

/** 主色阶的十个档位，顺序固定 */
const STOPS = ['50', '100', '200', '300', '400', '450', '500', '600', '800', '900'] as const

/**
 * 外观：主题 + 字号。
 *
 * 主题只切 `html[data-theme]`，配色与装饰都在 themes.css 里；
 * 字号走 zoom，同时写 `--ods-zoom` 让 fixed 布局按倍率反算高度，
 * 否则 100dvh 被放大后底部输入框会被裁掉。
 */
export const applyAppearance = () => {
  const { skin, fontScale, themeAuto, apiBaseUrl } = useSettings.getState()
  const root = document.documentElement

  const resolved = selectTheme({ skin, themeAuto, apiBaseUrl })

  if (resolved === 'plain') {
    delete root.dataset.theme
  } else {
    root.dataset.theme = resolved
  }

  // 配色同时写成行内变量：行内样式优先级最高，不依赖 CSS 选择器能否匹配上，
  // 避免「选了主题但界面没变」这类由选择器/缓存引起的问题。
  const theme = themeById(resolved)
  for (const stop of STOPS) {
    const color = theme.palette?.[stop]
    if (color) {
      root.style.setProperty(`--dsw-static-blue-${stop}`, color)
    } else {
      root.style.removeProperty(`--dsw-static-blue-${stop}`)
    }
  }
  if (theme.image) {
    root.style.setProperty('--ods-image', `url('/media/${theme.image}')`)
  } else {
    root.style.removeProperty('--ods-image')
  }
  root.style.setProperty('--ods-zoom', String(fontScale))
  root.style.zoom = fontScale === 1 ? '' : String(fontScale)
}

/** 当前生效主题（考虑自动匹配），组件里用 `useSettings(selectTheme)` 读 */
export const selectTheme = (state: {
  skin: string
  themeAuto: boolean
  apiBaseUrl: string
}): ThemeId => {
  const manual = isThemeId(state.skin) ? state.skin : DEFAULT_THEME
  if (!state.themeAuto) {
    return manual
  }
  return matchTheme(THEMES, { apiBaseUrl: state.apiBaseUrl }) ?? manual
}

/** 监听设置变化，自动套用主题与字号 */
export const setupAppearance = () => {
  applyAppearance()
  useSettings.subscribe((state, prev) => {
    if (
      state.skin !== prev.skin ||
      state.fontScale !== prev.fontScale ||
      state.themeAuto !== prev.themeAuto ||
      state.apiBaseUrl !== prev.apiBaseUrl
    ) {
      applyAppearance()
    }
  })
}
