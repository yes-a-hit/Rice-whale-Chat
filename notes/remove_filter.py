import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# =========================================================
# 1. reply.ts：安全拒绝不再丢弃已下发的思考与正文
# =========================================================
p = root / "src/services/chat/reply.ts"
t = io.open(p, encoding="utf-8").read()

old = """/**
 * 回复结束：未结束的思考块以当前时间收尾。
 * 安全拒绝（stop_reason: refusal）时已下发的思考与正文不能撤回，按协议要求由客户端丢弃，只保留工具块。
 */
export const settleReply = (
  reply: AssistantMessage,
  status: Extract<ReplyStatus, 'done' | 'stopped' | 'error'>,
  now: number,
  error?: AssistantMessage['error']
): AssistantMessage => ({
  ...reply,
  status,
  error,
  blocks: reply.blocks.flatMap((block): ReplyBlock[] => {
    if (reply.stopReason === 'refusal' && (block.type === 'thinking' || block.type === 'text')) {
      return []
    }
    return block.type === 'thinking' && block.startedAt !== undefined && block.endedAt === undefined
      ? [{ ...block, endedAt: now }]
      : [block]
  }),
})"""
new = """/**
 * 回复结束：未结束的思考块以当前时间收尾。
 * 官方 demo 会在 stop_reason 为 refusal 时丢弃已下发的思考与正文（按协议由客户端裁掉）；
 * 这里保留全部内容——服务端已经下发的字就是用户要看的字。
 */
export const settleReply = (
  reply: AssistantMessage,
  status: Extract<ReplyStatus, 'done' | 'stopped' | 'error'>,
  now: number,
  error?: AssistantMessage['error']
): AssistantMessage => ({
  ...reply,
  status,
  error,
  blocks: reply.blocks.map((block): ReplyBlock =>
    block.type === 'thinking' && block.startedAt !== undefined && block.endedAt === undefined
      ? { ...block, endedAt: now }
      : block
  ),
})"""
assert old in t
t = t.replace(old, new, 1)

# 续写：refusal 不再阻止
old = """  if (
    !reply.prefix ||
    reply.stopReason === 'refusal' ||
    reply.stopReason === 'tool_use' ||"""
new = """  if (
    !reply.prefix ||
    reply.stopReason === 'tool_use' ||"""
assert old in t
t = t.replace(old, new, 1)

# 上下文：refusal 轮次也回传
old = """  (message.status === 'done' || message.status === 'stopped') &&
  message.stopReason !== 'refusal' &&
  !message.blocks.some((block) => block.type === 'text' && block.isTemplate) &&"""
new = """  (message.status === 'done' || message.status === 'stopped') &&
  !message.blocks.some((block) => block.type === 'text' && block.isTemplate) &&"""
assert old in t
t = t.replace(old, new, 1)

t = t.replace(
    """/**
 * 已结束或停止且有回答文本的回复才放进上下文；被安全拒绝的轮次不回传。
 * 服务端模板提示不进入上下文。
 */""",
    """/**
 * 已结束或停止且有回答文本的回复才放进上下文。
 * 服务端模板提示不进入上下文。
 */""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("reply.ts ok")

# =========================================================
# 2. describe.ts：不再把 refusal 换成固定拒答文案
# =========================================================
p = root / "src/services/chat/describe.ts"
t = io.open(p, encoding="utf-8").read()
old = """  if (reply.stopReason === 'refusal') {
    // 导入的拒绝回复优先展示归档中的模板，普通正文仍不可展示。
    return { text: template || translate('replyRefused'), presentation: 'response' }
  }
"""
new = """  // stop_reason 为 refusal 时正文已经保留并正常展示，不再贴固定拒答话术。
"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("describe.ts ok")

# =========================================================
# 3. AssistantMessage.tsx：不隐藏正文与思考区
# =========================================================
p = root / "src/components/messages/AssistantMessage.tsx"
t = io.open(p, encoding="utf-8").read()
old = """  // 安全拒绝：已下发的思考与正文按协议丢弃，只显示模板答复。
  const refused = message.stopReason === 'refusal'
  const answer = refused ? null : view.answer"""
new = """  // 官方 demo 会把 refusal 轮的正文与思考整段藏起来；这里照常展示。
  const answer = view.answer"""
assert old in t
t = t.replace(old, new, 1)

old = """      {refused ? null : (
        <ReplyArea
          message={message}
          view={view}
          streaming={streaming}
          hasResponse={!!responseText}
        />
      )}"""
new = """      <ReplyArea
        message={message}
        view={view}
        streaming={streaming}
        hasResponse={!!responseText}
      />"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("AssistantMessage.tsx ok")
