import { useIsMobile } from '../../app/viewport.js'
import { useTranslate } from '../../i18n/index.js'
import { useSettings } from '../../services/settings.js'
import { selectTheme } from '../../app/skins.js'
import { themeAsset, themeById } from '../../app/themes/registry.js'
import { openSettings } from '../settings/settingsDialogState.js'
import { ChatInput } from '../chatInput/ChatInput.js'
import { MobileHeader } from './MobileHeader.js'
import styles from './Welcome.module.css'

/** 新对话：角色图 + 输入框。桌面端居中；移动端输入框吸底 */
export const Welcome = () => {
  const t = useTranslate()
  const isMobile = useIsMobile()
  const hasApiKey = useSettings((state) => Boolean(state.apiKey))
  const theme = useSettings(selectTheme)
  return (
    <div className={styles.container}>
      {isMobile ? <MobileHeader /> : null}
      <div className={styles.welcome}>
        <div className={styles.mascot}>
          {hasApiKey && !themeById(theme).builtinBubble ? (
            <div className={styles.bubble}>{t('odsWelcomeBubble')}</div>
          ) : null}
          <img
            className={styles.mascotImage}
            src={themeAsset(theme, hasApiKey ? 'welcome' : 'hungry')}
            alt={hasApiKey ? t('appName') : t('odsBalanceNoKey')}
            draggable={false}
          />
          {hasApiKey ? null : (
            <button
              type="button"
              className={styles.keyButton}
              onClick={() => openSettings('data')}
            >
              {t('odsWelcomeAddKey')}
            </button>
          )}
        </div>
        <ChatInput sessionId={null} />
        {isMobile ? <div className={styles.caveat}>{t('contentCaveat')}</div> : null}
      </div>
    </div>
  )
}
