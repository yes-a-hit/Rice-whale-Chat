import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 类型：加 edited 标记 ----------
p = root / "src/services/chat/types.ts"
t = io.open(p, encoding="utf-8").read()
if "edited?: boolean" not in t:
    t = t.replace(
        "  /** 最近一次请求的用量，续写后更新 */\n  usage?: MessageUsage",
        "  /** 用户手动改过正文（只改本地，不重新请求模型） */\n  edited?: boolean\n  /** 最近一次请求的用量，续写后更新 */\n  usage?: MessageUsage",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("types ok")

# ---------- 2. store：editReply / deleteMessage ----------
p = root / "src/services/chat/store.ts"
t = io.open(p, encoding="utf-8").read()

if "export const editReply" not in t:
    block = '''
/** 编辑助手回复：只改本地正文，不重新请求模型、不触发重新生成 */
export const editReply = (sessionId: string, messageId: string, content: string): boolean => {
  if (get().importingHistory || deletingSessions.has(sessionId) || getStreamController(sessionId)) {
    return false
  }
  const session = getSession(sessionId)
  if (!session) {
    return false
  }
  const path = getVisibleMessages(session)
  const message = path.find((item) => item.id === messageId)
  const text = content.trim()
  if (message?.role !== 'assistant' || !text) {
    return false
  }
  // 保留思考/工具块，把正文合并成一个 text 块
  const blocks: ReplyBlock[] = message.blocks.filter((block) => block.type !== 'text')
  blocks.push({ type: 'text', text })
  updateReply(sessionId, { ...message, blocks, edited: true })
  updateSession(sessionId, (s) => ({ ...s, updatedAt: Date.now() }))
  persist(sessionId)
  return true
}

/**
 * 删除一条消息。
 * 删助手回复时，连带它对应的那条提问一起删，避免留下孤零零的问题。
 */
export const deleteMessage = (sessionId: string, messageId: string): boolean => {
  if (get().importingHistory || deletingSessions.has(sessionId) || getStreamController(sessionId)) {
    return false
  }
  const session = getSession(sessionId)
  if (!session) {
    return false
  }
  const path = getVisibleMessages(session)
  const index = path.findIndex((item) => item.id === messageId)
  if (index < 0) {
    return false
  }
  const doomed = new Set([messageId])
  const previous = path[index - 1]
  if (path[index].role === 'assistant' && previous?.role === 'user') {
    doomed.add(previous.id)
  }
  updateSession(sessionId, (s) => ({
    ...s,
    messages: s.messages.filter((item) => !doomed.has(item.id)),
    updatedAt: Date.now(),
  }))
  persist(sessionId)
  return true
}
'''
    anchor = "export const selectMessageVersion = "
    assert anchor in t
    t = t.replace(anchor, block.lstrip("\n") + "\n" + anchor, 1)

if "ReplyBlock" not in t.split("export const")[0]:
    t = t.replace(
        "import type { ChatModel, CreateMessageRequest } from '../api/types.js'",
        "import type { ChatModel, CreateMessageRequest } from '../api/types.js'\nimport type { ReplyBlock } from './types.js'",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("store ok")
