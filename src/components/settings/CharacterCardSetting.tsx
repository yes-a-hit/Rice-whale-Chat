import { useRef, useState } from 'react'
import { useTranslate } from '../../i18n/index.js'
import { setCharacterPrompt, useSettings } from '../../services/settings.js'
import { buildCardSystemPrompt, parseCardFile } from '../../services/characterCard.js'
import { showToast } from '../base/toastState.js'
import { SettingCell } from './SettingCell.js'
import styles from './Ext.module.css'

/**
 * 角色卡：导入 PNG（内嵌 chara 数据）或 JSON（chara card v2/v3），
 * 转成系统提示词写入设置。清空即回到官方默认提示词。
 */
export const CharacterCardSetting = () => {
  const t = useTranslate()
  const characterPrompt = useSettings((state) => state.characterPrompt)
  const characterName = useSettings((state) => state.characterName)
  const inputRef = useRef<HTMLInputElement>(null)
  const [busy, setBusy] = useState(false)
  const current = characterName || characterPrompt.trim().split('\n')[0]?.slice(0, 40) || ''

  const onPick = async (file: File | undefined) => {
    if (!file) {
      return
    }
    setBusy(true)
    try {
      const card = await parseCardFile(file)
      setCharacterPrompt(buildCardSystemPrompt(card), card.name)
      showToast(t('odsCardImported', { name: card.name || t('odsCard') }))
    } catch (error) {
      showToast({
        key: 'odsCardImportFailed',
        params: { message: error instanceof Error ? error.message : String(error) },
      })
    } finally {
      setBusy(false)
      if (inputRef.current) {
        inputRef.current.value = ''
      }
    }
  }

  return (
    <SettingCell
      label={t('odsCard')}
      description={current ? t('odsCardCurrent', { text: current }) : t('odsCardHint')}
      status={null}
      stacked
      action={
        <div className={styles.fieldRow}>
          <input
            ref={inputRef}
            className={styles.hiddenFile}
            type="file"
            accept=".png,.json,image/png,application/json"
            onChange={(event) => void onPick(event.target.files?.[0])}
          />
          <button
            type="button"
            className={styles.saveButton}
            disabled={busy}
            onClick={() => inputRef.current?.click()}
          >
            {busy ? t('odsCardImporting') : t('odsCardImport')}
          </button>
          {characterPrompt.trim() ? (
            <button type="button" className={styles.ghostButton} onClick={() => setCharacterPrompt('', '')}>
              {t('odsCardClear')}
            </button>
          ) : null}
        </div>
      }
    />
  )
}
