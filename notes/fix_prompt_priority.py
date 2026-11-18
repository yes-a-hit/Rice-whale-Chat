import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 系统提示词优先于角色卡 ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
old = """ * 全局提示词与角色卡各自独立，同时存在时按「全局 → 角色卡」拼接；都为空才回落官方默认。
 */
export const resolveSystemPrompt = (): string => {
  const { systemPrompt, characterPrompt } = useSettings.getState()
  const parts = [systemPrompt.trim(), characterPrompt.trim()].filter(Boolean)
  return parts.length > 0 ? parts.join('\\n\\n') : DEFAULT_SYSTEM_PROMPT
}"""
new = """ * 系统提示词优先：填了系统提示词就只用它（角色卡不参与，避免两套设定打架）；
 * 系统提示词为空时才用角色卡；两者都空回落官方默认。
 */
export const resolveSystemPrompt = (): string => {
  const { systemPrompt, characterPrompt } = useSettings.getState()
  const global = systemPrompt.trim()
  if (global) {
    return global
  }
  const card = characterPrompt.trim()
  return card || DEFAULT_SYSTEM_PROMPT
}"""
assert old in t, "resolveSystemPrompt anchor missing"
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("prompt priority ok")
