import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- B1. 价格改成官方口径（元 / 百万 token） ----------
p = root / "src/services/billing.ts"
t = io.open(p, encoding="utf-8").read()
old_price = """export const DEFAULT_PRICE: PriceTable = {
  cacheHit: 0.2,
  input: 2,
  output: 3,
  search: 0.01,
}"""
new_price = """/**
 * DeepSeek 官方价（元 / 百万 token，缓存命中价 / 未命中输入价 / 输出价）。
 * 换模型或换服务商后可在设置里改。
 */
export const DEFAULT_PRICE: PriceTable = {
  cacheHit: 0.5,
  input: 2,
  output: 8,
  search: 0.01,
}"""
if old_price in t:
    t = t.replace(old_price, new_price, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("price ok")
else:
    print("price pattern miss")

# ---------- B2. 底部条：把正在生成的回复按字符估算进去 ----------
p = root / "src/components/billing/SessionStatsBar.tsx"
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    "import { compactNumber, formatCost, summarizeUsage } from '../../services/billing.js'",
    "import { compactNumber, DEFAULT_PRICE, formatCost, summarizeUsage } from '../../services/billing.js'\n"
    "import { getReplyText } from '../../services/chat/view.js'",
    1,
)

t = t.replace(
    "  const usage = useMemo(() => summarizeUsage(session?.messages ?? []), [session?.messages])",
    """  const usage = useMemo(() => {
    const messages = session?.messages ?? []
    const base = summarizeUsage(messages)
    // 流式回复还没有 usage 字段：按已生成字符数估 output token，让数字实时动
    const pending = messages.filter(
      (message) => message.role === 'assistant' && message.status === 'pending'
    )
    if (pending.length === 0) {
      return base
    }
    let liveTokens = 0
    for (const message of pending) {
      liveTokens += Math.ceil(getReplyText(message).length / 1.6)
    }
    if (liveTokens <= 0) {
      return base
    }
    const costOutput = (liveTokens / 1_000_000) * DEFAULT_PRICE.output
    return {
      ...base,
      outputTokens: base.outputTokens + liveTokens,
      totalTokens: base.totalTokens + liveTokens,
      costOutput: base.costOutput + costOutput,
      costTotal: base.costTotal + costOutput,
    }
  }, [session?.messages])""",
    1,
)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("stats bar ok")
