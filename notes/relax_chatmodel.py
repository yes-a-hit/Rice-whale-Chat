import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ChatModel 放宽为 string：第三方 OpenAI 兼容服务的模型名不受限
p = root / "src/services/api/types.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """/**
 * 可选模型。
 * - v4.1-flash：快速档，便宜、快，日常问答
 * - v4-pro：专家档，慢但推理强，适合复杂问题
 */
export type ChatModel = 'deepseek-v4.1-flash' | 'deepseek-v4-pro'""",
    """/**
 * 模型名。DeepSeek 官方两档：
 * - deepseek-v4.1-flash：快速档，便宜、快，日常问答
 * - deepseek-v4-pro：专家档，慢但推理强，适合复杂问题
 * 接第三方 OpenAI 兼容接口时可以是任意模型名，所以类型放宽为 string。
 */
export type ChatModel = string""",
    1,
)
t = t.replace(
    "export const CHAT_MODELS: { id: ChatModel; labelKey: 'odsModelFlash' | 'odsModelPro' }[] = [",
    "export const CHAT_MODELS: { id: string; labelKey: 'odsModelFlash' | 'odsModelPro' }[] = [",
    1,
)
t = t.replace(
    "export const DEFAULT_CHAT_MODEL: ChatModel = 'deepseek-v4.1-flash'",
    "export const DEFAULT_CHAT_MODEL = 'deepseek-v4.1-flash'",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("types ok")

# initialModel 也放宽
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """const initialModel = (): ChatModel =>
  read(KEYS.model) === 'deepseek-v4-pro' ? 'deepseek-v4-pro' : 'deepseek-v4.1-flash'""",
    """const initialModel = (): string => read(KEYS.model) || 'deepseek-v4.1-flash'""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("initialModel ok")
