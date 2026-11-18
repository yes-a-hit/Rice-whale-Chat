import { useMemo } from 'react'
import { useTranslate } from '../../i18n/index.js'
import { useSettings } from '../../services/settings.js'
import { useChatStore } from '../../services/chat/store.js'
import { compactNumber, formatCost, summarizeUsage } from '../../services/billing.js'
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
  const usage = useMemo(() => summarizeUsage(session?.messages ?? []), [session?.messages])

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
