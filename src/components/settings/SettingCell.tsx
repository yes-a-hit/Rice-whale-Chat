import clsx from 'clsx'
import type { ReactNode } from 'react'
import { useTranslate, type TranslationKey, type TranslationMessage } from '../../i18n/index.js'
import { BackupError } from '../../services/chat/backup.js'
import styles from './Settings.module.css'

/** `reason` 为失败原因的文案 key，展示时按当前语言翻译后填入 `message` 参数。 */
export type Status = (TranslationMessage & { error?: boolean; reason?: TranslationKey }) | null

/** 失败附带原因：预期的错误用对应文案作原因，其他错误用错误信息。 */
export const errorStatus = (key: TranslationKey, error: unknown): Status => ({
  key,
  ...(error instanceof BackupError
    ? { reason: error.key }
    : { params: { message: error instanceof Error ? error.message : String(error) } }),
  error: true,
})

/** 设置项一行：左侧标题与说明，右侧操作控件 */
export const SettingCell = ({
  label,
  description,
  status,
  action,
  className,
  stacked = false,
}: {
  label: string
  description?: string
  status: Status
  action: ReactNode
  className?: string
  /** 操作控件换行占满整行（多行输入、长文本框） */
  stacked?: boolean
}) => {
  const t = useTranslate()
  return (
    <div className={clsx(styles.cell, !stacked && styles.row, className)}>
      <div className={styles.text}>
        <div className={styles.label}>{label}</div>
        {status || description ? (
          <div className={clsx(styles.description, status?.error && styles.error)}>
            {status
              ? t(status.key, status.reason ? { message: t(status.reason) } : status.params)
              : description}
          </div>
        ) : null}
      </div>
      {action}
    </div>
  )
}
