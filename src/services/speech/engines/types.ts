/** 朗读引擎统一接口：三种实现（系统语音 / 本地模型 / 云端 TTS）都产出同一种行为 */

export type SpeakContext = {
  /** 中止信号：用户停止、切换会话、发送新消息 */
  signal: AbortSignal
  /** 第一段声音开始播放（用于把 loading 切成 playing） */
  onStart: () => void
}

export type SpeakOptions = {
  /** 云端音色 id，本地/系统引擎忽略 */
  cloudVoice?: 'stella' | 'tide'
  /** 本地模型路径（已下载的模型缓存 key） */
  localModel?: string
  /** 设备偏好 */
  device?: 'auto' | 'npu' | 'gpu' | 'cpu'
}

export interface TtsEngine {
  readonly id: 'system' | 'kokoro' | 'cloud'
  /** 是否已具备运行条件（模型已下载、API Key 存在等） */
  isReady(): Promise<boolean>
  /** 播报整段文本；abort 时静默结束，不抛错 */
  speak(text: string, ctx: SpeakContext, options?: SpeakOptions): Promise<void>
}
