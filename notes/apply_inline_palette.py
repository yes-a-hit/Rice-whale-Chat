import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. applyAppearance：把调色板写成行内变量 ----------
p = root / "src/app/skins.ts"
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    """import { useSettings } from '../services/settings.js'
import { matchTheme } from './themes/types.js'
import { DEFAULT_THEME, isThemeId, THEMES } from './themes/registry.js'
import type { ThemeId } from './themes/types.js'""",
    """import { useSettings } from '../services/settings.js'
import { matchTheme } from './themes/types.js'
import { DEFAULT_THEME, isThemeId, THEMES, themeById } from './themes/registry.js'
import type { ThemeId } from './themes/types.js'

/** 主色阶的十个档位，顺序固定 */
const STOPS = ['50', '100', '200', '300', '400', '450', '500', '600', '800', '900'] as const""",
    1,
)

t = t.replace(
    """  const resolved = selectTheme({ skin, themeAuto, apiBaseUrl })

  if (resolved === 'plain') {
    delete root.dataset.theme
  } else {
    root.dataset.theme = resolved
  }""",
    """  const resolved = selectTheme({ skin, themeAuto, apiBaseUrl })

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
  }""",
    1,
)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("skins ok")
