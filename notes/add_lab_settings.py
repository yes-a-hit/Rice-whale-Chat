import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- settings：imageProvider ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
if "imageProvider" not in t:
    t = t.replace(
        "export type ModelSource =",
        "export type ImageProvider = 'cloud' | 'local'\n\nexport type ModelSource =",
        1,
    )
    t = t.replace(
        "  imageModel: string",
        "  imageModel: string\n  /** 生图走云端 BYOK 还是本地 NPU 通道 */\n  imageProvider: ImageProvider",
        1,
    )
    t = t.replace(
        "  imageModel: 'ods:image-model',",
        "  imageModel: 'ods:image-model',\n  imageProvider: 'ods:image-provider',",
        1,
    )
    t = t.replace(
        "  imageModel: read(KEYS.imageModel) ?? DEFAULT_IMAGE_MODEL,",
        "  imageModel: read(KEYS.imageModel) ?? DEFAULT_IMAGE_MODEL,\n"
        "  imageProvider: read(KEYS.imageProvider) === 'local' ? 'local' : 'cloud',",
        1,
    )
    t = t.replace(
        "export const setImageModel =",
        """export const setImageProvider = (imageProvider: ImageProvider) => {
  write(KEYS.imageProvider, imageProvider)
  useSettings.setState({ imageProvider })
}

export const setImageModel =""",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("imageProvider ok")

# ---------- ExtSettings：把本地模型相关搬走 ----------
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()

# VoiceSettings 只剩 ASR + 语速音色
start = t.index("const VoiceSettings = () => {")
end = t.index("const ImageSettings = () => {")
new_voice = """const VoiceSettings = () => {
  const t = useTranslate()
  const asrEngine = useSettings((state) => state.asrEngine)
  return (
    <>
      <SettingCell
        label={t('odsAsrEngine')}
        description={t('odsAsrEngineHint')}
        status={null}
        action={
          <Select<AsrEngine>
            ariaLabel={t('odsAsrEngine')}
            value={asrEngine}
            options={[
              { value: 'system', label: t('odsAsrSystem') },
              { value: 'local', label: t('odsAsrLocal') },
              { value: 'cloud', label: t('odsAsrCloud') },
            ]}
            onChange={setAsrEngine}
          />
        }
      />
      <TtsFineTuning />
    </>
  )
}

"""
t = t[:start] + new_voice + t[end:]

t = t.replace("    <VoiceSettings />\n    <ModelsSection />\n", "    <VoiceSettings />\n", 1)

# 清理不再使用的 import
for line in (
    "  setComputeDevice,\n",
    "  setModelSource,\n",
    "  setTtsEngine,\n",
    "  type ComputeDevice,\n",
    "  type ModelSource,\n",
    "  type TtsEngine,\n",
    "import { ModelsSection } from './ModelsSection.js'\n",
    "import { detectCapabilities, resolveBackend, type ComputeCapabilities } from '../../services/device.js'\n",
):
    t = t.replace(line, "", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ExtSettings trimmed")
