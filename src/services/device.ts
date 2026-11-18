/**
 * 本地推理能力探测。
 *
 * 浏览器里能拿到的加速通道只有 WebNN（navigator.ml）与 WebGPU，
 * 手机上 Hexagon / Apple ANE 这类 NPU 一般只开放给原生运行时，
 * 因此这里如实报告能力，由引擎按 `auto` 顺序降级，而不是谎报 NPU 可用。
 */

export type ComputeCapabilities = {
  /** WebNN 是否存在 */
  webnn: boolean
  /** WebNN 是否存在 NPU 设备类型（部分浏览器会把 cpu/gpu 映射进来） */
  webnnNpu: boolean
  /** WebGPU 是否存在 */
  webgpu: boolean
  /** WebAssembly SIMD 是否可用 */
  wasmSimd: boolean
  /** 线程数（WASM 多线程） */
  hardwareConcurrency: number
  /** 实际会使用的后端 */
  resolved: 'npu' | 'gpu' | 'cpu'
}

type NavigatorWithML = Navigator & {
  ml?: { createContext?: unknown }
  gpu?: { requestAdapter?: unknown }
}

const detectWebnnNpu = async (): Promise<boolean> => {
  const ml = (navigator as NavigatorWithML).ml
  if (!ml || typeof ml.createContext !== 'function') {
    return false
  }
  try {
    const context = await (
      ml.createContext as (options: unknown) => Promise<{ destroy?: () => void }>
    )({ deviceType: 'npu' })
    context.destroy?.()
    return true
  } catch {
    return false
  }
}

export const detectCapabilities = async (): Promise<ComputeCapabilities> => {
  const nav = navigator as NavigatorWithML
  const webnn = !!nav.ml && typeof nav.ml.createContext === 'function'
  const webgpu = !!nav.gpu && typeof nav.gpu.requestAdapter === 'function'
  const webnnNpu = webnn ? await detectWebnnNpu() : false
  let wasmSimd = false
  try {
    // 16 字节 SIMD 探测：支持时该模块可编译
    wasmSimd = WebAssembly.validate(
      new Uint8Array([
        0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x05, 0x01, 0x60, 0x00, 0x01, 0x7b,
        0x03, 0x02, 0x01, 0x00, 0x0a, 0x0a, 0x01, 0x08, 0x00, 0xfd, 0x0c, 0x00, 0x00, 0x00, 0x00,
        0x0b,
      ])
    )
  } catch {
    wasmSimd = false
  }
  const resolved: ComputeCapabilities['resolved'] = webnnNpu ? 'npu' : webgpu ? 'gpu' : 'cpu'
  return {
    webnn,
    webnnNpu,
    webgpu,
    wasmSimd,
    hardwareConcurrency: navigator.hardwareConcurrency || 1,
    resolved,
  }
}

/** 按用户偏好与实际情况选后端：auto 时 npu → gpu → cpu */
export const resolveBackend = (
  preference: 'auto' | 'npu' | 'gpu' | 'cpu',
  caps: ComputeCapabilities
): ComputeCapabilities['resolved'] => {
  switch (preference) {
    case 'npu':
      return caps.webnnNpu ? 'npu' : caps.webgpu ? 'gpu' : 'cpu'
    case 'gpu':
      return caps.webgpu ? 'gpu' : 'cpu'
    case 'cpu':
      return 'cpu'
    default:
      return caps.resolved
  }
}
