import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. resolveSystemPrompt 恢复顺序拼接 ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
old = """ * 系统提示词优先：填了系统提示词就只用它（角色卡不参与，避免两套设定打架）；
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
new = """ * 分层拼接：系统提示词在前，角色卡在后（顺序固定，后者是「人设补充」，不覆盖前者）；
 * 两者都空时回落官方默认。
 */
export const resolveSystemPrompt = (): string => {
  const { systemPrompt, characterPrompt } = useSettings.getState()
  const parts = [systemPrompt.trim(), characterPrompt.trim()].filter(Boolean)
  return parts.length > 0 ? parts.join('\\n\\n') : DEFAULT_SYSTEM_PROMPT
}"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("system prompt order ok")
