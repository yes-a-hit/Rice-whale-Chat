import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- device.ts：把「为什么没有 NPU」讲清楚 ----------
p = root / "src/services/device.ts"
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    """  /** 线程数（WASM 多线程） */
  hardwareConcurrency: number""",
    """  /** 线程数（WASM 多线程） */
  hardwareConcurrency: number
  /** 原生桥是否已装（装了才有资格谈真 NPU） */
  nativeBridge: boolean""",
    1,
)
t = t.replace(
    """  const resolved: ComputeCapabilities['resolved'] = webnnNpu ? 'npu' : webgpu ? 'gpu' : 'cpu'
  return {
    webnn,
    webnnNpu,
    webgpu,
    wasmSimd,
    hardwareConcurrency: navigator.hardwareConcurrency || 1,
    resolved,
  }""",
    """  const resolved: ComputeCapabilities['resolved'] = webnnNpu ? 'npu' : webgpu ? 'gpu' : 'cpu'
  return {
    webnn,
    webnnNpu,
    webgpu,
    wasmSimd,
    hardwareConcurrency: navigator.hardwareConcurrency || 1,
    nativeBridge: Boolean((globalThis as { RiceWhaleBridge?: unknown }).RiceWhaleBridge),
    resolved,
  }""",
    1,
)
t = t.rstrip() + """

/**
 * 为什么手机明明有 NPU，检测却显示没有。
 *
 * 这不是手机的问题，是**浏览器层没有通往 NPU 的通道**：
 *
 * 1. Android WebView 不支持 WebNN（Chromium 在 WebView 里关掉了该特性）；
 * 2. Chrome for Android 即使有 WebNN，也只暴露 `cpu` 与 `gpu` 两个 deviceType——
 *    `npu` 目前只在 ChromeOS、Windows Copilot+ 这类带 ML Service 的平台上；
 * 3. 骁龙 Hexagon 的入口是 QNN SDK / SNPE / NNAPI，都只能从原生代码调用。
 *
 * 所以 Web 侧能拿到的全部算力是：WebGPU（Adreno）> WASM SIMD。想真吃 NPU，
 * 必须写 Capacitor 原生插件（Kotlin + ONNX Runtime Mobile + QNN EP），
 * 再把结果通过 `globalThis.RiceWhaleBridge` 暴露给 JS。
 */
export const explainCompute = (caps: ComputeCapabilities): string => {
  if (caps.nativeBridge) {
    return 'native'
  }
  if (!caps.webnn) {
    return 'no-webnn'
  }
  if (!caps.webnnNpu) {
    return 'no-npu-device'
  }
  return 'npu'
}
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("device ok")

# ---------- LabSettings：检测结果分情况说明 ----------
p = root / "src/components/settings/LabSettings.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """        description={
          caps
            ? t('odsDetectResult', {
                npu: caps.webnnNpu ? '✓' : '✗',
                gpu: caps.webgpu ? '✓' : '✗',
                simd: caps.wasmSimd ? '✓' : '✗',
                resolved: resolveBackend(computeDevice, caps),
                cores: caps.hardwareConcurrency,
              })
            : t('odsComputeDeviceHint')
        }""",
    """        description={
          caps
            ? `WebNN ${caps.webnn ? '✓' : '✗'} · NPU ${caps.webnnNpu ? '✓' : '✗'} · WebGPU ${
                caps.webgpu ? '✓' : '✗'
              } · SIMD ${caps.wasmSimd ? '✓' : '✗'} · ${caps.hardwareConcurrency} 线程 → 实际 ${resolveBackend(
                computeDevice,
                caps
              )}\\n${t(
                explainCompute(caps) === 'native'
                  ? 'odsNpuNativeReady'
                  : explainCompute(caps) === 'no-webnn'
                    ? 'odsNpuNoWebnn'
                    : explainCompute(caps) === 'no-npu-device'
                      ? 'odsNpuNoDevice'
                      : 'odsNpuOk'
              )}`
            : t('odsComputeDeviceHint')
        }""",
    1,
)
t = t.replace(
    "import { detectCapabilities, resolveBackend, type ComputeCapabilities } from '../../services/device.js'",
    "import {\n  detectCapabilities,\n  explainCompute,\n  resolveBackend,\n  type ComputeCapabilities,\n} from '../../services/device.js'",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("lab detect ok")
