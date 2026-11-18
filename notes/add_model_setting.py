import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- C1. 模型 id 改成 v4.1-flash / v4-pro ----------
p = root / "src/services/api/types.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "export type ChatModel = 'deepseek-flash' | 'deepseek-v4-pro'",
    """/**
 * 可选模型。
 * - v4.1-flash：快速档，便宜、快，日常问答
 * - v4-pro：专家档，慢但推理强，适合复杂问题
 */
export type ChatModel = 'deepseek-v4.1-flash' | 'deepseek-v4-pro'

/** 界面上给两档起的名字 */
export const CHAT_MODELS: { id: ChatModel; labelKey: 'odsModelFlash' | 'odsModelPro' }[] = [
  { id: 'deepseek-v4.1-flash', labelKey: 'odsModelFlash' },
  { id: 'deepseek-v4-pro', labelKey: 'odsModelPro' },
]

export const DEFAULT_CHAT_MODEL: ChatModel = 'deepseek-v4.1-flash'""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("types ok")

# ---------- C2. settings 加 model ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
if "  model: ChatModel" not in t:
    t = t.replace(
        "  collapseThinking: boolean",
        "  collapseThinking: boolean\n  /** 当前模型（Lite 用快速/专家两档，Plus 可任选） */\n  model: ChatModel",
        1,
    )
    t = t.replace(
        "  collapseThinking: read(KEYS.collapseThinking) === 'true',",
        "  collapseThinking: read(KEYS.collapseThinking) === 'true',\n  model: initialModel(),",
        1,
    )
    t = t.replace(
        "  collapseThinking: 'ods:collapse-thinking',",
        "  collapseThinking: 'ods:collapse-thinking',\n  model: 'ods:model',",
        1,
    )
    t = t.replace(
        "export const setCollapseThinking = ",
        """/** 模型 id 校验：只认 CHAT_MODELS 里的，旧值回落默认 */
const initialModel = (): ChatModel => {
  const value = read(KEYS.model)
  return CHAT_MODELS.some((item) => item.id === value) ? (value as ChatModel) : DEFAULT_CHAT_MODEL
}

export const setModel = (model: ChatModel) => {
  write(KEYS.model, model)
  useSettings.setState({ model })
}

export const setCollapseThinking = """,
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("settings ok")
