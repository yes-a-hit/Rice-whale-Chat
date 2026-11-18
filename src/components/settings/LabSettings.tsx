import { useState } from 'react'
import clsx from 'clsx'
import { Select } from '../base/Select.js'
import { useTranslate } from '../../i18n/index.js'
import {
  setAdvancedTts,
  setComputeDevice,
  setImageProvider,
  setModelSource,
  setTtsEngine,
  useSettings,
  type ComputeDevice,
  type ImageProvider,
  type ModelSource,
  type TtsEngine,
} from '../../services/settings.js'
import {
  detectCapabilities,
  explainCompute,
  resolveBackend,
  type ComputeCapabilities,
} from '../../services/device.js'
import { isLocalImageAvailable } from '../../services/image/localPipeline.js'
import { readNpuProviders, readNpuStatus } from '../../services/npu.js'
import { SettingCell } from './SettingCell.js'
import { ModelsSection } from './ModelsSection.js'
import styles from './Ext.module.css'

/**
 * 实验性玩法：本地模型、NPU 推理、进阶语音。
 *
 * 这一组默认全部关掉，开了也不保证能用——
 * Android WebView 里 WebNN 拿不到 Hexagon NPU，本地推理落在 WebGPU/WASM 上，
 * 有的机型直接起不来。所以单独放一页，出问题不影响日常聊天。
 */
export const NpuBridgeCell = () => {
  const [status, setStatus] = useState<Awaited<ReturnType<typeof readNpuStatus>> | null>(null)
  const [providers, setProviders] = useState<string[]>([])
  const [busy, setBusy] = useState(false)

  const probe = () => {
    setBusy(true)
    void Promise.all([readNpuStatus(), readNpuProviders()])
      .then(([next, list]) => {
        setStatus(next)
        setProviders(list)
      })
      .finally(() => setBusy(false))
  }

  const summary = status
    ? status.unavailable
      ? '未在原生环境运行（浏览器预览）'
      : `ORT ${status.ort ? '✓' : '✗'} · QNN ${status.qnnLibrary ? '✓' : '✗'} · ${status.soc || status.device} · ${status.abi}`
    : '查看 ONNX Runtime 与 QNN 后端是否打进包'

  return (
    <SettingCell
      label="NPU 原生桥"
      description={providers.length > 0 ? `${summary}\nEP: ${providers.join(', ')}` : summary}
      status={null}
      stacked
      action={
        <div className={styles.fieldRow}>
          <button type="button" className={styles.ghostButton} disabled={busy} onClick={probe}>
            {busy ? '检测中…' : '检测'}
          </button>
        </div>
      }
    />
  )
}

export const LabSettings = () => {
  const t = useTranslate()
  const ttsEngine = useSettings((state) => state.ttsEngine)
  const computeDevice = useSettings((state) => state.computeDevice)
  const modelSource = useSettings((state) => state.modelSource)
  const advancedTts = useSettings((state) => state.advancedTts)
  const imageProvider = useSettings((state) => state.imageProvider)
  const [caps, setCaps] = useState<ComputeCapabilities | null>(null)
  const [detecting, setDetecting] = useState(false)

  return (
    <>
      <div className={styles.group}>
        <div className={styles.groupTitle}>{t('odsLabTitle')}</div>
        <div className={styles.groupHint}>{t('odsLabHint')}</div>
      </div>

      <NpuBridgeCell />

      <SettingCell
        label={t('odsComputeDevice')}
        description={
          caps
            ? `WebNN ${caps.webnn ? '✓' : '✗'} · NPU ${caps.webnnNpu ? '✓' : '✗'} · WebGPU ${
                caps.webgpu ? '✓' : '✗'
              } · SIMD ${caps.wasmSimd ? '✓' : '✗'} · ${caps.hardwareConcurrency} 线程 → 实际 ${resolveBackend(
                computeDevice,
                caps
              )}\n${t(
                explainCompute(caps) === 'native'
                  ? 'odsNpuNativeReady'
                  : explainCompute(caps) === 'no-webnn'
                    ? 'odsNpuNoWebnn'
                    : explainCompute(caps) === 'no-npu-device'
                      ? 'odsNpuNoDevice'
                      : 'odsNpuOk'
              )}`
            : t('odsComputeDeviceHint')
        }
        status={null}
        stacked
        action={
          <div className={styles.fieldRow}>
            <Select<ComputeDevice>
              ariaLabel={t('odsComputeDevice')}
              value={computeDevice}
              options={[
                { value: 'auto', label: t('odsDeviceAuto') },
                { value: 'npu', label: t('odsDeviceNpu') },
                { value: 'gpu', label: t('odsDeviceGpu') },
                { value: 'cpu', label: t('odsDeviceCpu') },
              ]}
              onChange={setComputeDevice}
            />
            <button
              type="button"
              className={styles.ghostButton}
              disabled={detecting}
              onClick={() => {
                setDetecting(true)
                void detectCapabilities()
                  .then(setCaps)
                  .finally(() => setDetecting(false))
              }}
            >
              {detecting ? t('odsDetecting') : t('odsDetect')}
            </button>
          </div>
        }
      />

      <SettingCell
        label={t('odsTtsEngine')}
        description={t('odsLabTtsHint')}
        status={null}
        action={
          <Select<TtsEngine>
            ariaLabel={t('odsTtsEngine')}
            value={ttsEngine}
            options={[
              { value: 'system', label: t('odsTtsSystem') },
              { value: 'kokoro', label: t('odsTtsKokoro') },
              { value: 'cloud', label: t('odsTtsCloud') },
            ]}
            onChange={setTtsEngine}
          />
        }
      />

      <SettingCell
        label={t('odsAdvancedTts')}
        description={t('odsAdvancedTtsHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={advancedTts}
            className={clsx(styles.switch, advancedTts && styles.switchOn)}
            onClick={() => setAdvancedTts(!advancedTts)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />

      <SettingCell
        label={t('odsLocalImage')}
        description={
          isLocalImageAvailable() ? t('odsLocalImageReady') : t('odsLocalImageHint')
        }
        status={null}
        action={
          <Select<ImageProvider>
            ariaLabel={t('odsLocalImage')}
            value={imageProvider}
            options={[
              { value: 'cloud', label: t('odsImageCloud') },
              { value: 'local', label: t('odsImageLocal') },
            ]}
            onChange={setImageProvider}
          />
        }
      />

      <SettingCell
        label={t('odsModelSource')}
        description={t('odsModelSourceHint')}
        status={null}
        action={
          <Select<ModelSource>
            ariaLabel={t('odsModelSource')}
            value={modelSource}
            options={[
              { value: 'hf-mirror', label: t('odsSourceHfMirror') },
              { value: 'huggingface', label: t('odsSourceHf') },
              { value: 'kaggle', label: t('odsSourceKaggle') },
              { value: 'manual', label: t('odsSourceManual') },
            ]}
            onChange={setModelSource}
          />
        }
      />

      <ModelsSection />
    </>
  )
}
