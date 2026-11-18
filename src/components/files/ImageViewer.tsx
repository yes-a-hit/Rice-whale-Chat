import clsx from 'clsx'
import { useEffect } from 'react'
import { useTranslate } from '../../i18n/index.js'
import { IconCloseFill14 } from '../base/icons.js'
import styles from './ImageViewer.module.css'

/**
 * 应用内图片查看器。
 *
 * 原来点图片走 `window.open(url, '_blank')`，在 Capacitor WebView 里会开一个
 * 没有尺寸约束的新页面，图片按原始像素铺满并盖住界面。这里改成自绘的全屏层：
 * 图片按 contain 缩放到视口内，点任意处或右上角关闭。
 */
export const ImageViewer = ({ src, alt, onClose }: { src: string; alt?: string; onClose: () => void }) => {
  const t = useTranslate()

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  return (
    <div className={clsx(styles.overlay)} role="dialog" aria-modal="true" onClick={onClose}>
      <button type="button" className={styles.close} aria-label={t('close')} onClick={onClose}>
        <IconCloseFill14 />
      </button>
      <img
        className={styles.image}
        src={src}
        alt={alt ?? ''}
        draggable={false}
        onClick={(event) => event.stopPropagation()}
      />
    </div>
  )
}
