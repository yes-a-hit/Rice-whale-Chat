import { IconMenuOutline20, IconNewChatOutline20, IconSettingsOutline16 } from '../base/icons.js'
import { useTranslate } from '../../i18n/index.js'
import { newChat } from '../../services/chat/store.js'
import { IconButton } from '../base/IconButton.js'
import { openMobileSider } from '../sider/mobileSiderState.js'
import { openSettings } from '../settings/settingsDialogState.js'
import styles from './MobileHeader.module.css'

/** 移动端顶栏：左侧菜单打开侧边栏；会话页再显示标题与开启新对话 */
export const MobileHeader = ({ title }: { title?: string }) => {
  const t = useTranslate()
  return (
    <div className={styles.header}>
      <IconButton
        size="xl"
        tone="primary"
        icon={<IconMenuOutline20 />}
        aria-label={t('expandSiderbarButton')}
        onClick={openMobileSider}
      />
      {title === undefined ? null : (
        <>
          <div className={styles.title}>{title}</div>
          <IconButton
            size="xl"
            tone="primary"
            icon={<IconNewChatOutline20 />}
            aria-label={t('newChat')}
            onClick={newChat}
          />
        </>
      )}
      {/* 手机上唯一的常驻设置入口：任何页面都能进 */}
      <IconButton
        className={styles.settings}
        size="xl"
        tone="primary"
        icon={<IconSettingsOutline16 />}
        aria-label={t('settings')}
        onClick={() => openSettings('general')}
      />
    </div>
  )
}
