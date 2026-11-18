import { registerPlugin } from '@capacitor/core'

/**
 * 原生 NPU 桥（Android）。
 *
 * 浏览器层拿不到 Hexagon：WebView 不支持 WebNN，Chrome for Android 的 WebNN 也只有
 * cpu/gpu。所以真 NPU 只能走原生：ONNX Runtime Mobile + QNN Execution Provider，
 * 由 NpuPlugin.java 暴露给 JS。
 *
 * 这里只负责「报告状态」，模型加载与推理在后续版本接。
 */
export type NpuStatus = {
  /** onnxruntime 是否打进了包 */
  ort: boolean
  /** QNN HTP 后端库能否加载 */
  qnnLibrary: boolean
  /** 首选 ABI */
  abi: string
  abis: string[]
  device: string
  manufacturer: string
  sdk: number
  soc: string
  socManufacturer: string
  /** 浏览器端（非原生）调用时会有这个 */
  unavailable?: boolean
}

type NpuPluginShape = {
  available(): Promise<NpuStatus>
  providers(): Promise<{ providers: string[]; error?: string }>
}

const Npu = registerPlugin<NpuPluginShape>('Npu')

const FALLBACK: NpuStatus = {
  ort: false,
  qnnLibrary: false,
  abi: '',
  abis: [],
  device: '',
  manufacturer: '',
  sdk: 0,
  soc: '',
  socManufacturer: '',
  unavailable: true,
}

/** 读取原生桥状态；在浏览器里跑时返回 unavailable，不抛错 */
export const readNpuStatus = async (): Promise<NpuStatus> => {
  try {
    return await Npu.available()
  } catch {
    return FALLBACK
  }
}

/** 列出 ORT 编译进来的 Execution Provider（qnn / nnapi / cpu ...） */
export const readNpuProviders = async (): Promise<string[]> => {
  try {
    const result = await Npu.providers()
    return result.providers ?? []
  } catch {
    return []
  }
}
