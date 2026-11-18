import { useSettings } from '../settings.js'
import { generateLocalImage } from './localPipeline.js'

/**
 * 生图：BYOK，OpenAI 兼容的 `/images/generations` 接口。
 * 支持返回 b64_json（默认）或 url；结果统一转成 data URL 供界面预览与保存。
 */

export class ImageError extends Error {
  constructor(
    message: string,
    readonly status?: number
  ) {
    super(message)
    this.name = 'ImageError'
  }
}

export type GenerateOptions = {
  prompt: string
  /** 形如 "1024x1024" */
  size?: string
  signal?: AbortSignal
}

type Response = {
  data?: { b64_json?: string; url?: string }[]
  error?: { message?: string }
}

export const isImageReady = () => {
  const { imageEnabled, imageApiKey, imageBaseUrl, imageProvider } = useSettings.getState()
  if (!imageEnabled) {
    return false
  }
  // 本地通道不吃 BYOK，等原生桥接通才算就绪
  if (imageProvider === 'local') {
    return false
  }
  return Boolean(imageApiKey) && Boolean(imageBaseUrl)
}

export const generateImage = async ({
  prompt,
  size = '1024x1024',
  signal,
}: GenerateOptions): Promise<{ dataUrl: string; source: 'b64' | 'url' | 'local' }> => {
  const { imageBaseUrl, imageApiKey, imageModel, imageProvider } = useSettings.getState()

  if (imageProvider === 'local') {
    const result = await generateLocalImage({ prompt, size, signal })
    return { dataUrl: result.dataUrl, source: 'local' }
  }

  if (!imageApiKey) {
    throw new ImageError('image api key is empty')
  }
  const base = imageBaseUrl.trim().replace(/\/+$/, '')
  const response = await fetch(`${base}/images/generations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${imageApiKey}`,
    },
    body: JSON.stringify({
      model: imageModel || 'gpt-image-1',
      prompt,
      n: 1,
      size,
      response_format: 'b64_json',
    }),
    signal,
  })

  const payload = (await response.json().catch(() => null)) as Response | null
  if (!response.ok) {
    throw new ImageError(payload?.error?.message ?? `HTTP ${response.status}`, response.status)
  }
  const item = payload?.data?.[0]
  if (!item) {
    throw new ImageError('empty response')
  }
  if (item.b64_json) {
    return { dataUrl: `data:image/png;base64,${item.b64_json}`, source: 'b64' as const }
  }
  if (item.url) {
    return { dataUrl: item.url, source: 'url' as const }
  }
  throw new ImageError('no image in response')
}

/** 把生成结果存成文件，交给系统下载/相册 */
export const saveImage = async (dataUrl: string, filename = `ods-${Date.now()}.png`) => {
  const link = document.createElement('a')
  link.href = dataUrl
  link.download = filename
  link.rel = 'noopener'
  document.body.appendChild(link)
  link.click()
  link.remove()
}
