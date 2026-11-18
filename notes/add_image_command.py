import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 生图弹窗支持预填提示词 ----------
p = root / "src/components/image/imageDialogState.ts"
io.open(p, "w", encoding="utf-8", newline="\n").write(
    """import { create } from 'zustand'

/** 生图弹窗：open 控制显示，prompt 是打开时预填的提示词（指令触发用） */
export const useImageDialog = create(() => ({ open: false, prompt: '' }))

export const openImageDialog = (prompt = '') =>
  useImageDialog.setState({ open: true, prompt })

export const closeImageDialog = () => useImageDialog.setState({ open: false, prompt: '' })
"""
)
print("dialog state ok")

# ---------- 2. generateImage 走本地通道 ----------
p = root / "src/services/image/generate.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { useSettings } from '../settings.js'",
    "import { useSettings } from '../settings.js'\nimport { generateLocalImage } from './localPipeline.js'",
    1,
)
t = t.replace(
    """export const isImageReady = () => {
  const { imageEnabled, imageApiKey, imageBaseUrl } = useSettings.getState()
  return imageEnabled && Boolean(imageApiKey) && Boolean(imageBaseUrl)
}""",
    """export const isImageReady = () => {
  const { imageEnabled, imageApiKey, imageBaseUrl, imageProvider } = useSettings.getState()
  if (!imageEnabled) {
    return false
  }
  // 本地通道不吃 BYOK，等原生桥接通才算就绪
  if (imageProvider === 'local') {
    return false
  }
  return Boolean(imageApiKey) && Boolean(imageBaseUrl)
}""",
    1,
)
t = t.replace(
    """export const generateImage = async ({ prompt, size = '1024x1024', signal }: GenerateOptions) => {
  const { imageBaseUrl, imageApiKey, imageModel } = useSettings.getState()""",
    """export const generateImage = async ({
  prompt,
  size = '1024x1024',
  signal,
}: GenerateOptions): Promise<{ dataUrl: string; source: 'b64' | 'url' | 'local' }> => {
  const { imageBaseUrl, imageApiKey, imageModel, imageProvider } = useSettings.getState()

  if (imageProvider === 'local') {
    const result = await generateLocalImage({ prompt, size, signal })
    return { dataUrl: result.dataUrl, source: 'local' }
  }
""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("generate ok")

# ---------- 3. /img 指令触发 ----------
p = root / "src/components/chatInput/ChatInput.tsx"
t = io.open(p, encoding="utf-8").read()
old = """  const send = () => {
    if (
      useChatStore.getState().importingHistory ||"""
new = """  const send = () => {
    // 指令触发：/img 或 /draw 开头直接弹生图，不发给模型
    const raw = getDraft(sessionId)?.text?.trim() ?? ''
    const command = /^\\/(img|draw|pic)\\s+([\\s\\S]+)$/i.exec(raw)
    if (command && uiMode === 'plus') {
      openImageDialog(command[2].trim())
      setDraft(sessionId, { text: '' })
      void clearDraftText(sessionId)
      return
    }
    if (
      useChatStore.getState().importingHistory ||"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("command ok")
