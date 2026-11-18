import type { SpeakContext, TtsEngine } from './types.js'

/**
 * 本地模型 TTS：Kokoro-82M（ONNX）在设备上跑，优先 NPU（WebNN）→ WebGPU → WASM。
 *
 * 这条通道要等模型下载器与推理运行时接入后才有音频输出；
 * 现在保持接口就位，调用时给出可理解的错误，不静默失败。
 */
export const kokoroTts: TtsEngine = {
  id: 'kokoro',
  isReady: async () => false,
  speak: async (_text: string, _ctx: SpeakContext) => {
    throw new Error('LOCAL_TTS_NOT_INSTALLED')
  },
}
