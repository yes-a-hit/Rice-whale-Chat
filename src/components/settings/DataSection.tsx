import { useEffect, useState } from 'react'
import { useTranslate } from '../../i18n/index.js'
import { useSettings } from '../../services/settings.js'
import { fetchBalance, formatBalance, type Balance } from '../../services/api/balance.js'
import {
  clearAttachmentCache,
  formatBytesText,
  readLocalStats,
  type LocalStats,
} from '../../services/storage.js'
import { showToast } from '../base/toastState.js'
import { SettingCell } from './SettingCell.js'
import ext from './Ext.module.css'

/** 账户余额：BYOK 时最关心的一个数，进数据管理就能看到 */
const BalanceCell = () => {
  const t = useTranslate()
  const apiKey = useSettings((state) => state.apiKey)
  const showBalance = useSettings((state) => state.showBalance)
  const [balance, setBalance] = useState<Balance | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const refresh = () => {
    if (!apiKey || loading) {
      return
    }
    setLoading(true)
    setError('')
    void fetchBalance()
      .then(setBalance)
      .catch((reason: unknown) => {
        setBalance(null)
        setError(reason instanceof Error ? reason.message : String(reason))
      })
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    if (showBalance) {
      refresh()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showBalance, apiKey])

  if (!showBalance) {
    return null
  }

  const text = !apiKey
    ? t('odsBalanceNoKey')
    : loading
      ? t('odsBalanceLoading')
      : error
        ? t('odsBalanceFailed', { message: error })
        : balance
          ? `${formatBalance(balance)}${balance.is_available ? '' : ` · ${t('odsBalanceUnavailable')}`}`
          : t('odsBalanceHint')

  return (
    <SettingCell
      label={t('odsBalance')}
      description={text}
      status={null}
      stacked
      action={
        <button type="button" className={ext.saveButton} disabled={loading || !apiKey} onClick={refresh}>
          {t('odsBalanceRefresh')}
        </button>
      }
    />
  )
}

/** 本地数据库：占用与清理 */
const LocalDbCell = () => {
  const t = useTranslate()
  const [stats, setStats] = useState<LocalStats | null>(null)
  const [busy, setBusy] = useState(false)

  const refresh = () => {
    void readLocalStats()
      .then(setStats)
      .catch(() => setStats(null))
  }

  useEffect(refresh, [])

  const statText = stats
    ? t('odsLocalDbStats', {
        sessions: stats.sessions,
        messages: stats.messages,
        usage: stats.usage === null ? '—' : formatBytesText(stats.usage),
        quota: stats.quota === null ? '—' : formatBytesText(stats.quota),
      })
    : t('odsLocalDbLoading')

  return (
    <>
      <SettingCell
        label={t('odsLocalDb')}
        description={statText}
        status={null}
        stacked
        action={
          <div className={ext.fieldRow}>
            <button type="button" className={ext.ghostButton} onClick={refresh}>
              {t('odsLocalDbRefresh')}
            </button>
            <button
              type="button"
              className={ext.ghostButton}
              disabled={busy}
              onClick={() => {
                setBusy(true)
                void clearAttachmentCache()
                  .then(() => {
                    showToast(t('odsCacheCleared'))
                    refresh()
                  })
                  .finally(() => setBusy(false))
              }}
            >
              {t('odsClearCache')}
            </button>
          </div>
        }
      />
    </>
  )
}

export const DataSection = () => (
  <>
    <BalanceCell />
    <LocalDbCell />
  </>
)
