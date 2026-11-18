import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- initialNumber 辅助 + setter ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()

if "const initialNumber" not in t:
    t = t.replace(
        "const initialModelSource = (): ModelSource => {",
        """/** 读一个可空的数字设置；空字符串或非法值返回 null（= 不发送该参数） */
const initialNumber = (key: string): number | null => {
  const raw = read(key)
  if (raw === null || raw.trim() === '') {
    return null
  }
  const value = Number(raw)
  return Number.isFinite(value) ? value : null
}

const initialModelSource = (): ModelSource => {""",
        1,
    )

if "setSendSafetyCheck" not in t:
    t = t.replace(
        "export const setImageEnabled = (imageEnabled: boolean) => {",
        """export const setSendSafetyCheck = (sendSafetyCheck: boolean) => {
  write(KEYS.sendSafetyCheck, String(sendSafetyCheck))
  useSettings.setState({ sendSafetyCheck })
}

/** 采样参数写 null 等于恢复服务端默认 */
export const setSamplingParam = (
  key: 'temperature' | 'topP' | 'maxOutputTokens',
  value: number | null
) => {
  const storageKey =
    key === 'temperature' ? KEYS.temperature : key === 'topP' ? KEYS.topP : KEYS.maxOutputTokens
  write(storageKey, value === null ? null : String(value))
  useSettings.setState({ [key]: value } as never)
}

export const setImageEnabled = (imageEnabled: boolean) => {""",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("setters ok")

# ---------- 请求体组装 ----------
p = root / "src/services/chat/store.ts"
t = io.open(p, encoding="utf-8").read()
old = """            tools: serverTools(initial.search ?? false),"""
new = """            tools: serverTools(initial.search ?? false),
            ...(useSettings.getState().sendSafetyCheck ? { safety_check: SAFETY_CHECK } : {}),
            ...(useSettings.getState().temperature !== null
              ? { temperature: useSettings.getState().temperature as number }
              : {}),
            ...(useSettings.getState().topP !== null
              ? { top_p: useSettings.getState().topP as number }
              : {}),
            ...(useSettings.getState().maxOutputTokens !== null
              ? { max_tokens: useSettings.getState().maxOutputTokens as number }
              : {}),"""
assert old in t
t = t.replace(old, new, 1)

# 原有硬编码的 safety_check 那一行去掉（改由上面的展开控制）
old2 = """            safety_check: SAFETY_CHECK,
"""
assert old2 in t
t = t.replace(old2, "", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("request body ok")
