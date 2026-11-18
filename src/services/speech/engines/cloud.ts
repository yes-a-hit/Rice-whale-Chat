import { synthesize, TTS_SAMPLE_RATE } from '../../api/speech.js'
import { useSettings } from '../../settings.js'
import type { SpeakContext, SpeakOptions, TtsEngine } from './types.js'

/** 首帧前多缓冲一点，减少网络抖动造成的断续 */
const START_DELAY = 0.1

/** 16-bit 小端 PCM 转成 Float32；奇数字节留到下一段 */
const toFloat32 = (bytes: Uint8Array) => {
  const samples = new Float32Array(bytes.length >> 1)
  const view = new DataView(bytes.buffer, bytes.byteOffset, samples.length * 2)
  for (let i = 0; i < samples.length; i++) {
    samples[i] = view.getInt16(i * 2, true) / 0x8000
  }
  return samples
}

/**
 * 云端 TTS：走配置的服务地址 `/v1/tools/tts`，拿到 24kHz 裸 PCM，
 * 边收边用 AudioContext 排程播放，首帧到达即出声。
 */
export const cloudTts: TtsEngine = {
  id: 'cloud',
  isReady: async () => Boolean(useSettings.getState().apiKey),
  speak: async (text: string, ctx: SpeakContext, options?: SpeakOptions) => {
    const { apiKey, ttsVoice } = useSettings.getState()
    const context = new AudioContext({ sampleRate: TTS_SAMPLE_RATE })
    let nextTime = 0
    let lastSource: AudioBufferSourceNode | null = null
    let rest = new Uint8Array(0)
    let started = false
    try {
      const stream = await synthesize(apiKey ?? '', text, options?.cloudVoice ?? ttsVoice, ctx.signal)
      const reader = stream.getReader()
      ctx.signal.addEventListener('abort', () => void reader.cancel().catch(() => {}))
      for (;;) {
        const { done, value } = await reader.read()
        if (done) {
          break
        }
        const bytes = new Uint8Array(rest.length + value.length)
        bytes.set(rest)
        bytes.set(value, rest.length)
        const samples = toFloat32(bytes)
        rest = bytes.slice(samples.length * 2)
        if (samples.length === 0) {
          continue
        }
        const buffer = context.createBuffer(1, samples.length, TTS_SAMPLE_RATE)
        buffer.copyToChannel(samples, 0)
        const source = context.createBufferSource()
        source.buffer = buffer
        source.connect(context.destination)
        nextTime = Math.max(nextTime, context.currentTime + (lastSource ? 0 : START_DELAY))
        source.start(nextTime)
        nextTime += buffer.duration
        lastSource = source
        if (!started) {
          started = true
          ctx.onStart()
        }
      }
      if (lastSource) {
        await new Promise<void>((resolve) => {
          const source = lastSource as AudioBufferSourceNode
          source.onended = () => resolve()
          // 已停止时不会再触发 onended
          ctx.signal.addEventListener('abort', () => resolve(), { once: true })
        })
      }
    } finally {
      void context.close()
    }
  },
}
