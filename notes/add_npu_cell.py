import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/components/settings/LabSettings.tsx"
t = io.open(p, encoding="utf-8").read()

block = '''const NpuBridgeCell = () => {
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
      description={providers.length > 0 ? `${summary}\\nEP: ${providers.join(', ')}` : summary}
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

const LabSettings = () => {'''

t = t.replace("const LabSettings = () => {", block, 1)
t = t.replace(
    "import { isLocalImageAvailable } from '../../services/image/localPipeline.js'",
    "import { isLocalImageAvailable } from '../../services/image/localPipeline.js'\n"
    "import { readNpuProviders, readNpuStatus } from '../../services/npu.js'",
    1,
)
t = t.replace(
    "      <SettingCell\n        label={t('odsComputeDevice')}",
    "      <NpuBridgeCell />\n\n      <SettingCell\n        label={t('odsComputeDevice')}",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("npu cell ok")
