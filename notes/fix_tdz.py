import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\services\settings.ts")
t = io.open(p, encoding="utf-8").read()

# 去掉对 api/types 常量的依赖（模块初始化顺序会踩 TDZ），改用字面量
t = t.replace(
    """/** 模型 id 校验：只认 CHAT_MODELS 里的，旧值回落默认 */
const initialModel = (): ChatModel => {
  const value = read(KEYS.model)
  return CHAT_MODELS.some((item) => item.id === value) ? (value as ChatModel) : DEFAULT_CHAT_MODEL
}""",
    """/** 模型 id 校验：只认这两个，旧值回落快速档（不引用外部模块，避免初始化顺序问题） */
const initialModel = (): ChatModel =>
  read(KEYS.model) === 'deepseek-v4-pro' ? 'deepseek-v4-pro' : 'deepseek-v4.1-flash'""",
    1,
)
t = t.replace(
    """import {
  CHAT_MODELS,
  DEFAULT_CHAT_MODEL,
  type ChatModel,
} from './api/types.js'
""",
    "import type { ChatModel } from './api/types.js'\n",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settings de-cycled")
