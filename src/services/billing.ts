import type { AssistantMessage, Message } from './chat/types.js'

/**
 * 会话用量与计费。
 *
 * 数据来源：每条助手消息的 `usage`（接口在 message_start / message_delta 下发），
 * 以及消息上记录的生成耗时 `elapsedMs`。
 */

/** 单价：元 / 百万 token；search 为元 / 次 */
export type PriceTable = {
  cacheHit: number
  input: number
  output: number
  search: number
}

/** DeepSeek 官方价（deepseek-chat）：缓存命中 0.2、未命中 2、输出 3；联网检索按次估算 */
/**
 * DeepSeek 官方价（元 / 百万 token，缓存命中价 / 未命中输入价 / 输出价）。
 * 换模型或换服务商后可在设置里改。
 */
export const DEFAULT_PRICE: PriceTable = {
  cacheHit: 0.5,
  input: 2,
  output: 8,
  search: 0.01,
}

/** 上下文窗口，单位 token */
export const CONTEXT_LIMIT = 131_072

export type SessionUsage = {
  /** 对话轮数（助手消息条数） */
  turns: number
  /** 内容段数（思考 + 正文 + 工具） */
  steps: number
  /** 未命中缓存的输入 token */
  inputTokens: number
  /** 命中缓存的输入 token */
  cacheHitTokens: number
  /** 写入缓存的 token（首次请求时产生） */
  cacheCreationTokens: number
  outputTokens: number
  /** 联网检索次数 */
  searchRequests: number
  /** input + cacheHit + cacheCreation + output */
  totalTokens: number
  /** 缓存命中率：cacheHit / (cacheHit + input) */
  cacheHitRate: number
  /** 当前上下文占用：最近一轮的输入 + 输出 */
  contextUsed: number
  contextLimit: number
  contextRatio: number
  costInput: number
  costCacheHit: number
  costOutput: number
  costSearch: number
  cost: number
  /** 每秒输出 token（按有耗时的轮次加权） */
  tokensPerSecond: number
  /** 累计生成耗时（秒） */
  elapsedSeconds: number
}

const isAssistant = (message: Message): message is AssistantMessage => message.role === 'assistant'

export const summarizeUsage = (
  messages: Message[],
  price: PriceTable = DEFAULT_PRICE
): SessionUsage => {
  let turns = 0
  let steps = 0
  let inputTokens = 0
  let cacheHitTokens = 0
  let cacheCreationTokens = 0
  let outputTokens = 0
  let searchRequests = 0
  let elapsedMs = 0
  let lastContext = 0

  for (const message of messages) {
    if (!isAssistant(message)) {
      continue
    }
    turns += 1
    steps += message.blocks.length
    const usage = message.usage
    if (usage) {
      inputTokens += usage.input_tokens
      cacheHitTokens += usage.cache_read_input_tokens
      cacheCreationTokens += usage.cache_creation_input_tokens
      outputTokens += usage.output_tokens
      searchRequests += usage.server_tool_use?.web_search_requests ?? 0
    }
    if (message.elapsedMs && message.elapsedMs > 0) {
      elapsedMs += message.elapsedMs
    }
    if (usage && usage.output_tokens > 0) {
      // 最近一轮的上下文占用：输入（含缓存）+ 输出
      lastContext =
        usage.input_tokens +
        usage.cache_read_input_tokens +
        usage.cache_creation_input_tokens +
        usage.output_tokens
    }
  }

  const perMillion = 1_000_000
  const costInput = (inputTokens / perMillion) * price.input
  const costCacheHit = (cacheHitTokens / perMillion) * price.cacheHit
  const costOutput = (outputTokens / perMillion) * price.output
  const costSearch = searchRequests * price.search

  const promptTokens = cacheHitTokens + inputTokens
  const elapsedSeconds = elapsedMs / 1000

  return {
    turns,
    steps,
    inputTokens,
    cacheHitTokens,
    cacheCreationTokens,
    outputTokens,
    searchRequests,
    totalTokens: inputTokens + cacheHitTokens + cacheCreationTokens + outputTokens,
    cacheHitRate: promptTokens > 0 ? cacheHitTokens / promptTokens : 0,
    contextUsed: lastContext,
    contextLimit: CONTEXT_LIMIT,
    contextRatio: lastContext > 0 ? Math.min(1, lastContext / CONTEXT_LIMIT) : 0,
    costInput,
    costCacheHit,
    costOutput,
    costSearch,
    cost: costInput + costCacheHit + costOutput + costSearch,
    tokensPerSecond: elapsedSeconds > 0 ? outputTokens / elapsedSeconds : 0,
    elapsedSeconds,
  }
}

/** 把大数字压成 1.2K / 55.7M 这样的短文本 */
export const compactNumber = (value: number): string => {
  if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(value >= 10_000_000 ? 1 : 2)}M`
  }
  if (value >= 1000) {
    return `${(value / 1000).toFixed(value >= 10_000 ? 1 : 2)}K`
  }
  return String(Math.round(value))
}

/** 金额：小额保留两位，超出一元保留两位，不到一分钱显示 <¥0.01 */
export const formatCost = (value: number): string => {
  if (value <= 0) {
    return '¥0'
  }
  if (value < 0.01) {
    return '<¥0.01'
  }
  return `¥${value.toFixed(2)}`
}
