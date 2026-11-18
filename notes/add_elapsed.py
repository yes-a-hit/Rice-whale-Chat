import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. types：记录生成耗时 ----------
p = root / "src/services/chat/types.ts"
t = io.open(p, encoding="utf-8").read()
old = """  /** 最近一次请求的用量，续写后更新 */
  usage?: MessageUsage"""
new = """  /** 最近一次请求的用量，续写后更新 */
  usage?: MessageUsage
  /** 本轮从发请求到收尾的耗时（毫秒），用于算 token 速率 */
  elapsedMs?: number
  /** 请求发出时刻，settleReply 用它算 elapsedMs */
  startedAt?: number"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("types ok")

# ---------- 2. settleReply 计算耗时 ----------
p = root / "src/services/chat/reply.ts"
t = io.open(p, encoding="utf-8").read()
old = """): AssistantMessage => ({
  ...reply,
  status,
  error,
  blocks: reply.blocks.map((block): ReplyBlock =>"""
new = """): AssistantMessage => ({
  ...reply,
  status,
  error,
  elapsedMs: reply.elapsedMs ?? (reply.startedAt ? Math.max(0, now - reply.startedAt) : undefined),
  blocks: reply.blocks.map((block): ReplyBlock =>"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settleReply ok")

# ---------- 3. 新建回复时打时间戳 ----------
p = root / "src/services/chat/store.ts"
t = io.open(p, encoding="utf-8").read()
old = """    const reply: AssistantMessage = { ...previous, status: 'pending', error: undefined }"""
if old in t:
    new = """    const reply: AssistantMessage = {
      ...previous,
      status: 'pending',
      error: undefined,
      startedAt: Date.now(),
      elapsedMs: undefined,
    }"""
    t = t.replace(old, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("store startedAt ok")
else:
    print("store anchor missing, check manually")
