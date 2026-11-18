import { useMemo } from 'react'
import { useTranslate } from '../../i18n/index.js'
import { useChatStore } from '../../services/chat/store.js'
import { compactNumber, formatCost, summarizeUsage } from '../../services/billing.js'
import { SettingCell } from './SettingCell.js'
import styles from './Usage.module.css'

const COLORS = {
  cacheHit: '#16a34a',
  input: '#dc2626',
  output: '#2563eb',
  search: '#ea580c',
}

type Row = {
  key: string
  label: string
  color: string
  amount: string
  cost: string
  ratio: number
}

/** 设置 → 用量：四色堆叠条 + 明细 */
export const UsageSection = () => {
  const t = useTranslate()
  const session = useChatStore((state) =>
    state.activeId ? state.sessionCache[state.activeId] : undefined
  )
  const usage = useMemo(() => summarizeUsage(session?.messages ?? []), [session?.messages])

  if (usage.turns === 0) {
    return <p className={styles.empty}>{t('odsUsageEmpty')}</p>
  }

  const tokenTotal = Math.max(1, usage.cacheHitTokens + usage.inputTokens + usage.outputTokens)
  const rows: Row[] = [
    {
      key: 'cache',
      label: t('odsUsageCacheHit'),
      color: COLORS.cacheHit,
      amount: `${compactNumber(usage.cacheHitTokens)} ${t('odsUsageTokensUnit')}`,
      cost: formatCost(usage.costCacheHit),
      ratio: usage.cacheHitTokens / tokenTotal,
    },
    {
      key: 'input',
      label: t('odsUsageInput'),
      color: COLORS.input,
      amount: `${compactNumber(usage.inputTokens)} ${t('odsUsageTokensUnit')}`,
      cost: formatCost(usage.costInput),
      ratio: usage.inputTokens / tokenTotal,
    },
    {
      key: 'output',
      label: t('odsUsageOutput'),
      color: COLORS.output,
      amount: `${compactNumber(usage.outputTokens)} ${t('odsUsageTokensUnit')}`,
      cost: formatCost(usage.costOutput),
      ratio: usage.outputTokens / tokenTotal,
    },
    {
      key: 'search',
      label: t('odsUsageSearch'),
      color: COLORS.search,
      amount: `${usage.searchRequests} ${t('odsUsageTimesUnit')}`,
      cost: formatCost(usage.costSearch),
      // 检索按次计费，没有 token 数，条形里给一个最小可见段
      ratio: usage.searchRequests > 0 ? 0.02 : 0,
    },
  ]

  const visible = rows.filter((row) => row.ratio > 0)
  const sumRatio = visible.reduce((sum, row) => sum + row.ratio, 0) || 1

  return (
    <>
      <div className={styles.headline}>
        <span className={styles.total}>{formatCost(usage.cost)}</span>
        <span className={styles.sub}>
          {compactNumber(usage.totalTokens)} {t('odsUsageTokensUnit')} ·{' '}
          {t('odsStatsCache', { value: Math.round(usage.cacheHitRate * 100) })}
        </span>
      </div>

      <div className={styles.bar}>
        {visible.map((row) => (
          <span
            key={row.key}
            className={styles.segment}
            style={{ width: `${(row.ratio / sumRatio) * 100}%`, backgroundColor: row.color }}
            title={`${row.label} ${row.amount} ${row.cost}`}
          />
        ))}
      </div>

      <ul className={styles.legend}>
        {rows.map((row) => (
          <li key={row.key} className={styles.legendItem}>
            <span className={styles.swatch} style={{ backgroundColor: row.color }} />
            <span className={styles.legendLabel}>{row.label}</span>
            <span className={styles.legendAmount}>{row.amount}</span>
            <span className={styles.legendCost}>{row.cost}</span>
          </li>
        ))}
      </ul>

      <SettingCell
        label={t('odsUsageTotal')}
        description={t('odsUsagePriceHint')}
        status={null}
        action={<span className={styles.totalSmall}>{formatCost(usage.cost)}</span>}
      />
      <SettingCell
        label={t('odsUsageSpeed')}
        description={t('odsUsageElapsed')}
        status={null}
        action={
          <span className={styles.metric}>
            {Math.round(usage.tokensPerSecond)} tok/s · {usage.elapsedSeconds.toFixed(1)}s
          </span>
        }
      />
      <SettingCell
        label={t('odsUsageContext')}
        description={t('odsStatsContextHint')}
        status={null}
        action={<span className={styles.metric}>{Math.round(usage.contextRatio * 100)}%</span>}
      />
    </>
  )
}
