import { useEffect, useState } from 'react'
import { Button } from '../base/Button.js'
import { Modal } from '../base/Modal.js'
import { Select } from '../base/Select.js'
import { openSettings } from '../settings/settingsDialogState.js'
import { useTranslate } from '../../i18n/index.js'
import { useSettings } from '../../services/settings.js'
import { generateImage, saveImage } from '../../services/image/generate.js'
import { closeImageDialog, useImageDialog } from './imageDialogState.js'
import styles from './ImageDialog.module.css'

const SIZES = ['1024x1024', '1024x1536', '1536x1024']

/** 生图：填提示词 → 生成 → 预览与保存。仅在 Plus 模式提供 */
export const ImageDialog = () => {
  const t = useTranslate()
  const open = useImageDialog((state) => state.open)
  const seeded = useImageDialog((state) => state.prompt)
  const imageEnabled = useSettings((state) => state.imageEnabled)
  const [prompt, setPrompt] = useState('')
  const [size, setSize] = useState(SIZES[0])
  const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle')
  const [result, setResult] = useState<string | null>(null)
  const [error, setError] = useState('')

  // 指令触发（/img ...）时预填提示词
  useEffect(() => {
    if (open && seeded) {
      setPrompt(seeded)
    }
  }, [open, seeded])

  if (!open) {
    return null
  }

  const run = async () => {
    if (!prompt.trim() || status === 'loading') {
      return
    }
    setStatus('loading')
    setError('')
    try {
      const image = await generateImage({ prompt: prompt.trim(), size })
      setResult(image.dataUrl)
      setStatus('idle')
    } catch (reason) {
      setStatus('error')
      setError(reason instanceof Error ? reason.message : String(reason))
    }
  }

  return (
    <Modal
      title={t('odsImageDialogTitle')}
      onClose={closeImageDialog}
      footer={
        <>
          <Button variant="outlined" size="m" onClick={closeImageDialog}>
            {t('cancel')}
          </Button>
          {result ? (
            <Button variant="outlined" size="m" onClick={() => void saveImage(result)}>
              {t('odsImageSave')}
            </Button>
          ) : null}
          <Button variant="primary" size="m" disabled={status === 'loading'} onClick={() => void run()}>
            {status === 'loading' ? t('odsImageGenerating') : t('odsImageGenerate')}
          </Button>
        </>
      }
    >
      {imageEnabled ? (
        <div className={styles.body}>
          <textarea
            className={styles.prompt}
            rows={3}
            placeholder={t('odsImagePromptPlaceholder')}
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
          />
          <div className={styles.row}>
            <span className={styles.rowLabel}>{t('odsImageSize')}</span>
            <Select<string>
              ariaLabel={t('odsImageSize')}
              value={size}
              options={SIZES.map((value) => ({ value, label: value }))}
              onChange={setSize}
            />
          </div>
          {error ? <div className={styles.error}>{error}</div> : null}
          {result ? <img className={styles.preview} src={result} alt={prompt} /> : null}
        </div>
      ) : (
        <div className={styles.body}>
          <p className={styles.hint}>{t('odsImageNotConfigured')}</p>
          <Button
            variant="primary"
            size="m"
            onClick={() => {
              closeImageDialog()
              openSettings('ext')
            }}
          >
            {t('odsImageOpenSettings')}
          </Button>
        </div>
      )}
    </Modal>
  )
}
