/**
 * 本地（NPU）生图通道 —— 预留接口。
 *
 * 目标工作流（每一步都可换成原生实现，界面侧不用改）：
 *
 *   用户提示词
 *      │
 *      ▼  ① 提示词整理：0.5B 小语言模型（Qwen2.5-0.5B-Instruct / 同类）
 *           把中文口语化描述改写成带镜头、光线、画风的英文提示词 + 负面提示词
 *      ▼  ② 文本编码：CLIP（ViT-L/14 或 SD 自带的 CLIP text encoder）
 *      ▼  ③ 去噪：SD-Turbo 1.5B / SDXL-Turbo，1–4 步（turbo 蒸馏模型）
 *      ▼  ④ 解码：VAE → RGB 位图
 *      ▼  ⑤ 输出：写到指定目录，同时返回 data URL 给界面预览
 *
 * 现在只有接口：`isAvailable()` 恒 false，`generate()` 抛 LOCAL_IMAGE_NOT_INSTALLED。
 * 接上原生插件（ONNX Runtime Mobile + QNN EP，或 MNN / NCNN 的 Adreno 后端）后，
 * 把 `generate` 换成 bridge 调用即可，上层 `generateImage()` 与弹窗都不用动。
 */

export type LocalImageStage =
  | 'prompt'
  | 'clip'
  | 'diffusion'
  | 'vae'
  | 'write'

export type LocalImageOptions = {
  /** 用户原始提示词，中文口语也可以 */
  prompt: string
  /** 负面提示词，可空 */
  negativePrompt?: string
  /** 形如 "512x512" */
  size?: string
  /** 去噪步数，turbo 模型 1–4 步 */
  steps?: number
  /** 输出目录（原生侧可写路径）；空则用应用缓存目录 */
  outputDir?: string
  signal?: AbortSignal
  /** 每个阶段的进度回调，界面用来显示「正在 CLIP / 正在去噪 2/4」 */
  onStage?: (stage: LocalImageStage, ratio: number) => void
}

export type LocalImageResult = {
  dataUrl: string
  /** 原生侧落盘路径，WebView 里拿不到时为 undefined */
  filePath?: string
  /** 实际使用的提示词（小模型改写后的） */
  refinedPrompt?: string
}

export class LocalImageError extends Error {
  constructor(message: string, readonly stage?: LocalImageStage) {
    super(message)
    this.name = 'LocalImageError'
  }
}

/** 是否具备本地生图能力：需要原生桥 + 模型就位 */
export const isLocalImageAvailable = (): boolean => {
  const bridge = (globalThis as { RiceWhaleBridge?: { localImage?: unknown } }).RiceWhaleBridge
  return Boolean(bridge?.localImage)
}

export const generateLocalImage = async (options: LocalImageOptions): Promise<LocalImageResult> => {
  const bridge = (globalThis as {
    RiceWhaleBridge?: {
      localImage?: {
        generate: (payload: Record<string, unknown>) => Promise<LocalImageResult>
      }
    }
  }).RiceWhaleBridge

  if (!bridge?.localImage) {
    throw new LocalImageError('LOCAL_IMAGE_NOT_INSTALLED', 'prompt')
  }

  options.onStage?.('prompt', 0)
  return bridge.localImage.generate({
    prompt: options.prompt,
    negativePrompt: options.negativePrompt ?? '',
    size: options.size ?? '512x512',
    steps: options.steps ?? 4,
    outputDir: options.outputDir ?? '',
  })
}
