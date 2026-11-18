import type { SpeakContext, TtsEngine } from './types.js'

/**
 * 本地模型 TTS（Kokoro-82M，ONNX）。
 *
 * 现实情况：Android WebView 里 WebNN 拿不到 Hexagon NPU，本地推理只能落到
 * WebGPU（Adreno）或 WASM；WebGPU 在部分机型/驱动上初始化即失败，表现为「点了没声」。
 * 所以这里不假装能用——
 *   - 没接入推理运行时之前 `isReady()` 恒为 false；
 *   - 上层（readAloud.ts）检测到不可用会自动回落系统朗读，并提示一句。
 *
 * 真要吃 NPU 得走原生插件（ONNX Runtime Mobile + QNN EP），那部分在 NativeBridge 里预留。
 */
export const kokoroTts: TtsEngine = {
  id: 'kokoro',
  isReady: async () => false,
  speak: async (_text: string, _ctx: SpeakContext) => {
    throw new Error('LOCAL_TTS_NOT_INSTALLED')
  },
}
