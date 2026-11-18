import io, re, sys, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/services/api/client.ts"
text = io.open(p, encoding="utf-8").read()

old_head = """/** 构建期 API 地址，默认 https://api.deepseek.com；本地开发支持开发服务器代理 */
export const API_ORIGIN = __API_ORIGIN__
/** Anthropic 兼容接口的前缀 */
const ANTHROPIC_BASE_URL = `${API_ORIGIN}/anthropic/v1`"""

new_head = """/** 构建期默认 API 地址；运行时以设置中的 apiBaseUrl 为准，便于手机填中转地址 */
export const BUILD_API_ORIGIN = __API_ORIGIN__

/** 当前生效的 API 地址（去尾斜杠） */
export const getApiOrigin = (): string => {
  const custom = useSettings.getState().apiBaseUrl?.trim()
  return (custom || BUILD_API_ORIGIN).replace(/\\/+$/, '')
}

/** Anthropic 兼容接口的前缀（每次请求时按当前设置生成） */
const anthropicBaseUrl = () => `${getApiOrigin()}/anthropic/v1`"""

assert old_head in text, "head anchor missing"
text = text.replace(old_head, new_head)

import_line = "import { translate, type TranslationMessage } from '../../i18n/index.js'"
assert import_line in text
text = text.replace(
    import_line,
    import_line + "\nimport { useSettings } from '../settings.js'",
    1,
)

text = text.replace("${ANTHROPIC_BASE_URL}", "${anthropicBaseUrl()}")
text = text.replace("${API_ORIGIN}", "${getApiOrigin()}")

io.open(p, "w", encoding="utf-8", newline="\n").write(text)
print("patched client.ts")
