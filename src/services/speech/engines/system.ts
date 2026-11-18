import { useSettings } from '../../settings.js'
import { matchVoiceProfile, stripUnreadable } from '../contextVoice.js'
import type { SpeakContext, TtsEngine } from './types.js'

/**
 * 系统语音：直接用手机自带的 TTS（Android TTS 引擎 / iOS Siri 语音）。
 * 零配置、离线、不耗 token；缺点是音色由系统决定，长文本在部分浏览器会被截断，
 * 因此按句切分后顺序播报。
 */

const splitSentences = (text: string): string[] => {
  const normalized = text.replace(/\s+/g, ' ').trim()
  if (!normalized) {
    return []
  }
  // 中英文句末标点切句，单段不超过 120 字
  const parts = normalized.match(/[^。！？!?.;；\n]+[。！？!?.;；]?/g) ?? [normalized]
  const chunks: string[] = []
  let buffer = ''
  for (const part of parts) {
    if ((buffer + part).length > 120) {
      if (buffer) {
        chunks.push(buffer)
      }
      buffer = part.length > 120 ? '' : part
      if (part.length > 120) {
        for (let i = 0; i < part.length; i += 120) {
          chunks.push(part.slice(i, i + 120))
        }
      }
    } else {
      buffer += part
    }
  }
  if (buffer) {
    chunks.push(buffer)
  }
  return chunks
}

const pickVoice = (): SpeechSynthesisVoice | undefined => {
  const voices = window.speechSynthesis?.getVoices?.() ?? []
  const preferred = useSettings.getState().ttsSystemVoice
  if (preferred) {
    const hit = voices.find((voice) => voice.name === preferred)
    if (hit) {
      return hit
    }
  }
  const zh = voices.filter((voice) => voice.lang.toLowerCase().startsWith('zh'))
  // 优先本地（离线）中文语音，其次任意中文，最后系统默认
  return zh.find((voice) => voice.localService) ?? zh[0] ?? voices[0]
}

type SpeakTuning = { rate: number; pitch: number }

const speakOne = (text: string, voice: SpeechSynthesisVoice | undefined, tuning: SpeakTuning) =>
  new Promise<void>((resolve, reject) => {
    const utterance = new SpeechSynthesisUtterance(text)
    if (voice) {
      utterance.voice = voice
      utterance.lang = voice.lang
    }
    utterance.rate = tuning.rate
    utterance.pitch = tuning.pitch
    utterance.onend = () => resolve()
    utterance.onerror = (event) => {
      // 被取消不算失败
      if (event.error === 'canceled' || event.error === 'interrupted') {
        resolve()
      } else {
        reject(new Error(event.error || 'speechSynthesis failed'))
      }
    }
    window.speechSynthesis.speak(utterance)
  })

export const systemTts: TtsEngine = {
  id: 'system',
  isReady: async () => typeof window !== 'undefined' && 'speechSynthesis' in window,
  speak: async (text: string, ctx: SpeakContext) => {
    if (!('speechSynthesis' in window)) {
      throw new Error('speechSynthesis is not available on this device')
    }
    const { ttsRate, advancedTts } = useSettings.getState()
    // 进阶 TTS：按上下文挑语速/音高，并把代码、表格、链接换成口播话术
    const spoken = advancedTts ? stripUnreadable(text) : text
    const profile = advancedTts ? matchVoiceProfile(spoken, ttsRate) : null
    const tuning: SpeakTuning = { rate: profile?.rate ?? ttsRate, pitch: profile?.pitch ?? 1 }
    const chunks = splitSentences(spoken)
    if (chunks.length === 0) {
      return
    }
    const voice = pickVoice()
    let started = false
    for (const chunk of chunks) {
      if (ctx.signal.aborted) {
        window.speechSynthesis.cancel()
        return
      }
      if (!started) {
        started = true
        ctx.onStart()
      }
      await speakOne(chunk, voice, tuning)
    }
  },
}
