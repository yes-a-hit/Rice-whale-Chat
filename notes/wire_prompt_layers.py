import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- reply.ts：支持首轮注入辅助层 ----------
p = root / "src/services/chat/reply.ts"
t = io.open(p, encoding="utf-8").read()

old = """export const toRequestMessages = (
  history: Message[],
  question: UserMessage,
  prefix?: AssistantMessage,
  thinking = prefix?.thinking ?? false,
  latestReminder?: string
): MessageParam[] => {
  const messages: MessageParam[] = []"""
new = """export const toRequestMessages = (
  history: Message[],
  question: UserMessage,
  prefix?: AssistantMessage,
  thinking = prefix?.thinking ?? false,
  latestReminder?: string,
  auxBlock?: string
): MessageParam[] => {
  const messages: MessageParam[] = []
  // 辅助层只注入一次：历史里没有规则标记就插一对消息，之后随历史滚动
  if (auxBlock && !hasAuxInjected(history.map((message) => message.content ?? ''))) {
    messages.push({ role: 'user', content: auxBlock }, { role: 'assistant', content: '明白，按这套规则来。' })
  }"""
assert old in t
t = t.replace(old, new, 1)

# 补 import
if "promptLayers" not in t:
    lines = t.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("import ") and "from './" in line:
            lines.insert(i + 1, "import { hasAuxInjected } from './promptLayers.js'")
            break
    t = "\n".join(lines)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("reply ok")

# ---------- store.ts：传参 ----------
p = root / "src/services/chat/store.ts"
t = io.open(p, encoding="utf-8").read()
old = """        const messages = toRequestMessages(
          prepared.history,
          prepared.question,
          prepared.prefix,
          initial.thinking ?? false,
          latestReminder
        )"""
new = """        const messages = toRequestMessages(
          prepared.history,
          prepared.question,
          prepared.prefix,
          initial.thinking ?? false,
          latestReminder,
          buildAuxBlock()
        )"""
assert old in t
t = t.replace(old, new, 1)

if "buildAuxBlock" not in t.split("buildAuxBlock()")[0].split("\n")[-1]:
    pass
t = t.replace(
    "import { resolveSystemPrompt, useSettings } from '../settings.js'",
    "import { buildAuxBlock } from './promptLayers.js'\nimport { resolveSystemPrompt, useSettings } from '../settings.js'",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("store ok")
