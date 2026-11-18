import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- DEFAULT_SKIN 改成 plain ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace('export const DEFAULT_SKIN = ', 'export const DEFAULT_SKIN = ')
import re

t = re.sub(r"export const DEFAULT_SKIN = '[^']*'", "export const DEFAULT_SKIN = 'plain'", t)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("DEFAULT_SKIN:", [l for l in t.split("\n") if "DEFAULT_SKIN =" in l])

# ---------- skins.ts 增加选择器 ----------
p = root / "src/app/skins.ts"
t = io.open(p, encoding="utf-8").read()
if "selectTheme" not in t:
    t = t.replace(
        "/** 监听设置变化，自动套用主题与字号 */",
        """/** 当前生效主题（考虑自动匹配），组件里用 `useSettings(selectTheme)` 读 */
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

/** 监听设置变化，自动套用主题与字号 */""",
        1,
    )
    t = t.replace(
        "import { DEFAULT_THEME, isThemeId, THEMES } from './themes/registry.js'",
        "import { DEFAULT_THEME, isThemeId, THEMES } from './themes/registry.js'\nimport type { ThemeId } from './themes/types.js'",
        1,
    )
    # applyAppearance 复用 selectTheme
    t = t.replace(
        """  let resolved = isThemeId(skin) ? skin : DEFAULT_THEME
  // 自动模式：按当前接口地址/模型名匹配主题（kimi → 月兔，glm → 奶牛）
  if (themeAuto) {
    const matched = matchTheme(THEMES, { apiBaseUrl })
    if (matched) {
      resolved = matched
    }
  }""",
        """  const resolved = selectTheme({ skin, themeAuto, apiBaseUrl })""",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("selectTheme ok")

# ---------- Welcome 用主题素材 ----------
p = root / "src/components/session/Welcome.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "src={hasApiKey ? '/media/welcome.webp' : '/media/hungry.webp'}",
    "src={themeAsset(theme, hasApiKey ? 'welcome' : 'hungry')}",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("welcome src ok")
