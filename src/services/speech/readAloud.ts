import { create } from 'zustand'
import type { TranslationMessage } from '../../i18n/index.js'
import { ApiError } from '../api/client.js'
import { classifyApiError } from '../api/errors.js'
import { useSettings } from '../settings.js'
import { cloudTts } from './engines/cloud.js'
import { kokoroTts } from './engines/kokoro.js'
import { systemTts } from './engines/system.js'
import type { TtsEngine } from './engines/types.js'

/**
 * 朗读：同一时间只读一条回复。
 * 三种引擎共用一套播放状态：system（手机自带语音）/ kokoro（本地模型）/ cloud（官方接口）。
 * 状态：loading（已请求、未出声）→ playing → 结束回到 idle。
 */
export type ReadAloudStatus = 'idle' | 'loading' | 'playing'

type ReadAloudState = {
  /** 正在朗读的回复 id */
  messageId: string | null
  status: ReadAloudStatus
  /** 当前使用的引擎，用于界面上标注 */
  engine: TtsEngine['id'] | null
}

export const useReadAloud = create<ReadAloudState>(() => ({
  messageId: null,
  status: 'idle',
  engine: null,
}))

let current: { controller: AbortController } | null = null

const engineFor = (id: TtsEngine['id']): TtsEngine => {
  switch (id) {
    case 'system':
      return systemTts
    case 'kokoro':
      return kokoroTts
    default:
      return cloudTts
  }
}

const finish = (controller: AbortController) => {
  if (current?.controller !== controller) {
    return
  }
  current = null
  useReadAloud.setState({ messageId: null, status: 'idle', engine: null })
}

/** 停止当前朗读（发送、停止生成、切换会话等场景调用） */
export const stopReadAloud = () => {
  if (current) {
    const { controller } = current
    controller.abort()
    // 系统语音需要显式取消队列
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel()
    }
    finish(controller)
  }
}

export const describeReadAloudError = (error: unknown): TranslationMessage | string => {
  if (
    error instanceof Error &&
    (error.message === 'LOCAL_TTS_NOT_INSTALLED' || error.message === 'LOCAL_TTS_FALLBACK')
  ) {
    return { key: 'odsLocalTtsFallback' }
  }
  if (error instanceof Error && /speechSynthesis/i.test(error.message)) {
    return { key: 'odsSystemTtsUnavailable' }
  }
  if (error instanceof ApiError && error.kind === 'protocol') {
    return error.message
  }
  // 400 表示这段正文服务端无法合成，与其余失败区分开
  if (error instanceof ApiError && error.status === 400) {
    return { key: 'ttsUnavailable' }
  }
  switch (classifyApiError(error)) {
    case 'unauthorized':
      return { key: 'apiKeyInvalidRetry' }
    case 'insufficientBalance':
      return { key: 'insufficientBalance' }
    case 'rateLimited':
      return { key: 'rateLimited' }
    default:
      return { key: 'ttsFailed' }
  }
}

/**
 * 开始朗读一条回复的正文；同一条正在朗读时调用等于停止。
 * 必须在点击事件中同步调用：AudioContext / 语音队列需要用户手势才能出声。
 */
export const toggleReadAloud = (
  messageId: string,
  text: string,
  onError: (error: unknown) => void
) => {
  const reading = useReadAloud.getState().messageId
  stopReadAloud()
  if (reading === messageId) {
    return
  }
  const controller = new AbortController()
  current = { controller }
  const configured = useSettings.getState().ttsEngine
  // 本地模型引擎没接运行时之前必然不可用，直接回落系统朗读，不让用户点了没反应
  const engineId = configured === 'kokoro' ? 'system' : configured
  if (engineId !== configured) {
    onError(new Error('LOCAL_TTS_FALLBACK'))
  }
  useReadAloud.setState({ messageId, status: 'loading', engine: engineId })
  const engine = engineFor(engineId)
  const { computeDevice, apiBaseUrl } = useSettings.getState()

  void engine
    .speak(
      text,
      {
        signal: controller.signal,
        onStart: () => {
          if (useReadAloud.getState().status === 'loading') {
            useReadAloud.setState({ status: 'playing' })
          }
        },
      },
      { cloudVoice: useSettings.getState().ttsVoice, device: computeDevice, localModel: apiBaseUrl }
    )
    .then(() => finish(controller))
    .catch((error: unknown) => {
      if (!controller.signal.aborted) {
        finish(controller)
        onError(error)
      }
    })
}
