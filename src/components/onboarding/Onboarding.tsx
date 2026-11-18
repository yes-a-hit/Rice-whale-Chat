import { useState } from 'react'
import clsx from 'clsx'
import { useTranslate } from '../../i18n/index.js'
import { completeOnboarding, type UiMode } from '../../services/settings.js'
import { selectTheme } from '../../app/skins.js'
import { useSettings } from '../../services/settings.js'
import { themeAsset } from '../../app/themes/registry.js'
import styles from './Onboarding.module.css'

/**
 * 首次启动：选一个模式。
 * 给家人用的场景只点一次就进聊天，两个卡片都是整块可点。
 */
export const Onboarding = () => {
  const logo = themeAsset(useSettings(selectTheme), 'logo')
  const t = useTranslate()
  const [chosen, setChosen] = useState<UiMode | null>(null)
  const start = (mode: UiMode) => {
    if (chosen) {
      return
    }
    setChosen(mode)
    completeOnboarding(mode)
  }
  return (
    <div className={styles.overlay} role="dialog" aria-modal="true" aria-label={t('odsOnboardTitle')}>
      <div className={styles.panel}>
        <img className={styles.logo} src={logo} alt="" draggable={false} />
        <h1 className={styles.title}>{t('odsOnboardTitle')}</h1>
        <p className={styles.subtitle}>{t('odsOnboardSubtitle')}</p>
        <div className={styles.cards}>
          <button
            type="button"
            className={clsx(styles.card, chosen === 'lite' && styles.cardChosen)}
            onClick={() => start('lite')}
          >
            <span className={styles.cardIcon}>🌤️</span>
            <span className={styles.cardTitle}>{t('odsModeLite')}</span>
            <span className={styles.cardDesc}>{t('odsOnboardLiteDesc')}</span>
          </button>
          <button
            type="button"
            className={clsx(styles.card, chosen === 'plus' && styles.cardChosen)}
            onClick={() => start('plus')}
          >
            <span className={styles.cardIcon}>🧩</span>
            <span className={styles.cardTitle}>{t('odsModePlus')}</span>
            <span className={styles.cardDesc}>{t('odsOnboardPlusDesc')}</span>
          </button>
        </div>
        <p className={styles.hint}>{t('odsOnboardHint')}</p>
      </div>
    </div>
  )
}
