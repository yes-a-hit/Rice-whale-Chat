import type { ModelSource } from '../settings.js'

/**
 * 本地模型清单。
 * 所有文件都按「仓库 + 文件名」描述，下载地址由当前选择的源拼出来；
 * 国内默认走 hf-mirror，kaggle 预留给大模型（需要用户自己的数据集直链）。
 */

export type ModelFile = {
  /** 仓库内的相对路径，例如 onnx/model_quantized.onnx */
  path: string
  /** 字节数，用于进度与磁盘占用展示 */
  bytes: number
}

export type ModelSpec = {
  id: string
  /** 展示名 */
  name: string
  /** 用途，决定出现在哪个设置项里 */
  kind: 'tts' | 'asr'
  /** HuggingFace 仓库 id */
  repo: string
  files: ModelFile[]
  /** 运行时入口文件（下载完成后校验用） */
  entry: string
  description: string
}

const MB = 1024 * 1024

export const MODELS: ModelSpec[] = [
  {
    id: 'kokoro-82m-q8',
    name: 'Kokoro-82M（中文/英文 TTS，量化）',
    kind: 'tts',
    repo: 'onnx-community/Kokoro-82M-v1.0-ONNX',
    entry: 'onnx/model_quantized.onnx',
    description: '82M 参数，手机端可实时；配套音色文件一起下载。',
    files: [
      { path: 'onnx/model_quantized.onnx', bytes: 92 * MB },
      { path: 'voices/zf_xiaobei.bin', bytes: 0.5 * MB },
      { path: 'voices/zm_yunxi.bin', bytes: 0.5 * MB },
      { path: 'tokenizer.json', bytes: 2 * MB },
    ],
  },
  {
    id: 'whisper-base-q8',
    name: 'Whisper-base（本地语音识别，量化）',
    kind: 'asr',
    repo: 'onnx-community/whisper-base',
    entry: 'onnx/decoder_model_merged_quantized.onnx',
    description: '约 150MB，中文识别够用；完全离线。',
    files: [
      { path: 'onnx/encoder_model_quantized.onnx', bytes: 40 * MB },
      { path: 'onnx/decoder_model_merged_quantized.onnx', bytes: 60 * MB },
      { path: 'tokenizer.json', bytes: 2 * MB },
      { path: 'config.json', bytes: 0.01 * MB },
    ],
  },
]

export const getModel = (id: string): ModelSpec | undefined =>
  MODELS.find((model) => model.id === id)

/** 各下载源的地址模板 */
export const buildModelUrl = (source: ModelSource, repo: string, path: string): string => {
  switch (source) {
    case 'huggingface':
      return `https://huggingface.co/${repo}/resolve/main/${path}`
    case 'hf-mirror':
      return `https://hf-mirror.com/${repo}/resolve/main/${path}`
    case 'kaggle':
      // Kaggle 数据集需要用户自己的 dataset 直链，这里给出可替换的占位
      return `https://www.kaggle.com/api/v1/models/${repo}/resolve/main/${path}`
    default:
      return ''
  }
}

/** 缓存键：模型文件统一放在这个 CacheStorage 里 */
export const MODEL_CACHE = 'ods-models'

export const cacheKey = (source: ModelSource, repo: string, path: string) =>
  buildModelUrl(source, repo, path) || `local://${repo}/${path}`
