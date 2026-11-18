import { useEffect, useState } from 'react'
import clsx from 'clsx'
import { useTranslate } from '../../i18n/index.js'
import { useSettings } from '../../services/settings.js'
import { MODELS, getModel } from '../../services/models/registry.js'
import {
  deleteModel,
  downloadModel,
  getModelState,
  type DownloadProgress,
  type ModelState,
} from '../../services/models/downloader.js'
import { SettingCell } from './SettingCell.js'
import styles from './Ext.module.css'

const formatMB = (bytes: number) => `${Math.round(bytes / (1024 * 1024))} MB`

const ModelRow = ({ modelId }: { modelId: string }) => {
  const t = useTranslate()
  const source = useSettings((state) => state.modelSource)
  const model = getModel(modelId)
  const [state, setState] = useState<ModelState>('missing')
  const [progress, setProgress] = useState<DownloadProgress | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [controller, setController] = useState<AbortController | null>(null)

  useEffect(() => {
    let alive = true
    if (model) {
      void getModelState(model, source).then((next) => {
        if (alive) {
          setState(next)
        }
      })
    }
    return () => {
      alive = false
    }
  }, [model, source])

  if (!model) {
    return null
  }

  const total = model.files.reduce((sum, file) => sum + file.bytes, 0)
  const percent = progress ? Math.min(100, Math.round((progress.done / progress.total) * 100)) : 0

  const start = () => {
    const next = new AbortController()
    setController(next)
    setError(null)
    setProgress({ done: 0, total, current: '' })
    void downloadModel(modelId, source, setProgress, next.signal)
      .then(async () => setState(await getModelState(model, source)))
      .catch((reason: unknown) => {
        if (!next.signal.aborted) {
          setError(reason instanceof Error ? reason.message : String(reason))
        }
      })
      .finally(() => {
        setController(null)
        setProgress(null)
      })
  }

  const remove = () => {
    void deleteModel(modelId, source).then(() => setState('missing'))
  }

  const statusText = error
    ? error
    : progress
      ? t('odsModelDownloading', { percent })
      : state === 'ready'
        ? t('odsModelReady')
        : state === 'partial'
          ? t('odsModelPartial')
          : t('odsModelMissing', { size: formatMB(total) })

  return (
    <SettingCell
      label={model.name}
      description={`${model.description} · ${statusText}`}
      status={null}
      stacked
      action={
        <div className={styles.fieldRow}>
          {progress ? (
            <>
              <div className={styles.progressTrack}>
                <div className={styles.progressFill} style={{ width: `${percent}%` }} />
              </div>
              <button type="button" className={styles.ghostButton} onClick={() => controller?.abort()}>
                {t('cancel')}
              </button>
            </>
          ) : state === 'ready' ? (
            <button type="button" className={styles.ghostButton} onClick={remove}>
              {t('odsModelDelete')}
            </button>
          ) : (
            <button
              type="button"
              className={styles.saveButton}
              onClick={start}
              disabled={source === 'manual'}
            >
              {state === 'partial' ? t('odsModelResume') : t('odsModelDownload')}
            </button>
          )}
        </div>
      }
    />
  )
}

/** 模型管理：本地 TTS / ASR 的模型下载、续传与删除 */
export const ModelsSection = () => {
  const t = useTranslate()
  const source = useSettings((state) => state.modelSource)
  return (
    <div className={clsx(styles.group)}>
      <div className={styles.groupTitle}>{t('odsModels')}</div>
      <div className={styles.groupHint}>
        {t('odsModelsHint', {
          source:
            source === 'hf-mirror'
              ? 'hf-mirror'
              : source === 'huggingface'
                ? 'HuggingFace'
                : source === 'kaggle'
                  ? 'Kaggle'
                  : t('odsSourceManual'),
        })}
      </div>
      {MODELS.map((model) => (
        <ModelRow key={model.id} modelId={model.id} />
      ))}
    </div>
  )
}
