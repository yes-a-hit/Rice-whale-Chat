import { useMemo } from 'react'
import { useTranslate } from '../../i18n/index.js'
import { useSettings } from '../../services/settings.js'
import { useChatStore } from '../../services/chat/store.js'
import { compactNumber, DEFAULT_PRICE, formatCost, summarizeUsage } from '../../services/billing.js'
import type { AssistantMessage } from '../../services/chat/types.js'
import styles from './SessionStatsBar.module.css'

/**
 * 输入框下方的会话用量条（仅 Plus 模式）：
 * 轮数 · 段数 · token 速率 | token 总量 · 缓存命中率 | 金额 | 上下文占比
 */
export const SessionStatsBar = ({ sessionId }: { sessionId: string | null }) => {
  const t = useTranslate()
  const uiMode = useSettings((state) => state.uiMode)
  const session = useChatStore((state) =>
    sessionId ? state.sessionCache[sessionId] : undefined
  )
/** 粗略取一条回复已生成的正文长度（不含思考块） */
const replyTextLength = (message: unknown): number => {
  let length = 0
  const blocks = (message as { blocks?: AssistantMessage['blocks'] }).blocks ?? []
  for (const block of blocks) {
    if (block.type === 'text' && 'text' in block) {
      length += String(block.text ?? '').length
    }
  }
  return length
}

  const usage = useMemo(() => {
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
      liveTokens += Math.ceil(replyTextLength(message) / 1.6)
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
      cost: base.cost + costOutput,
    }
  }, [session?.messages])

  if (uiMode !== 'plus' || usage.turns === 0) {
    return null
  }

  const percent = Math.round(usage.contextRatio * 100)

  return (
    <div className={styles.bar}>
      <span className={styles.group}>
        <span>{t('odsStatsTurns', { count: usage.turns })}</span>
        <span className={styles.dot}>·</span>
        <span>{t('odsStatsSteps', { count: usage.steps })}</span>
        {usage.tokensPerSecond > 0 ? (
          <>
            <span className={styles.dot}>·</span>
            <span>{t('odsStatsSpeed', { value: Math.round(usage.tokensPerSecond) })}</span>
          </>
        ) : null}
      </span>

      <span className={styles.group}>
        <span>{t('odsStatsTokens', { value: compactNumber(usage.totalTokens) })}</span>
        <span className={styles.dot}>·</span>
        <span className={styles.cache}>
          {t('odsStatsCache', { value: Math.round(usage.cacheHitRate * 100) })}
        </span>
      </span>

      <span className={styles.cost}>{formatCost(usage.cost)}</span>

      <span className={styles.context} title={t('odsStatsContextHint')}>
        <span
          className={styles.ring}
          style={{ background: `conic-gradient(var(--dsw-alias-brand-primary) ${percent}%, transparent 0)` }}
        />
        {t('odsStatsContext', { value: percent })}
      </span>
    </div>
  )
}
