import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\billing\SessionStatsBar.tsx")
t = io.open(p, encoding="utf-8").read()

# getReplyText 不在 view.ts，直接在本地从 message 拼文本
t = t.replace(
    "import { getReplyText } from '../../services/chat/view.js'",
    "import type { AssistantMessage } from '../../services/chat/types.js'",
    1,
)
t = t.replace(
    "      liveTokens += Math.ceil(getReplyText(message).length / 1.6)",
    "      liveTokens += Math.ceil(replyTextLength(message) / 1.6)",
    1,
)
t = t.replace(
    "  const usage = useMemo(() => {",
    """/** 粗略取一条回复已生成的正文长度（不含思考块） */
const replyTextLength = (message: AssistantMessage): number => {
  let length = 0
  for (const block of message.blocks ?? []) {
    if (block.type === 'text' && 'text' in block) {
      length += String(block.text ?? '').length
    }
  }
  return length
}

  const usage = useMemo(() => {""",
    1,
)
# 成本字段名是 cost
t = t.replace("      costTotal: base.costTotal + costOutput,", "      cost: base.cost + costOutput,", 1)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("stats bar fixed")
