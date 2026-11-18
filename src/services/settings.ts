import { create } from 'zustand'
import type { TtsVoice } from './api/speech.js'
import { normalizeLocation, type UserLocation } from './location.js'

export type Locale = 'zh-CN' | 'en-US'

/** 主题偏好；默认跟随系统 */
export type ThemePreference = 'light' | 'dark' | 'system'

/** 界面模式：lite（老登模式，极简）与 plus（重度，全功能 + 扩展） */
export type UiMode = 'lite' | 'plus'

/** 朗读引擎：系统语音 / 本地模型 / 官方云 TTS */
export type TtsEngine = 'system' | 'kokoro' | 'cloud'

/** 本地推理设备：npu 优先，运行时按可用性降级 */
export type ComputeDevice = 'auto' | 'npu' | 'gpu' | 'cpu'

/** 语音输入引擎：系统听写 / 本地 whisper / 官方 ASR */
export type AsrEngine = 'system' | 'local' | 'cloud'

/** 模型下载源 */
export type ImageProvider = 'cloud' | 'local'

export type ModelSource = 'hf-mirror' | 'huggingface' | 'kaggle' | 'manual'

/** 本机设置，存 localStorage：API 与服务地址、模式、语言主题、语音、提示词、皮肤、生图 BYOK */
type Settings = {
  apiKey: string | null
  locale: Locale
  themePreference: ThemePreference
  location: UserLocation | null
  ttsVoice: TtsVoice
  thinking: boolean
  search: boolean
  siderCollapsed: boolean
  /** 界面模式 */
  uiMode: UiMode
  /** 是否已完成首启引导（选过模式） */
  onboarded: boolean
  /** 聊天服务地址（可填中转/反代），默认官方 */
  apiBaseUrl: string
  /** 全局系统提示词；空字符串表示使用官方内置提示 */
  systemPrompt: string
  /** 皮肤 id */
  skin: string
  /** 界面字号倍数，lite 模式默认放大 */
  fontScale: number
  /** 朗读引擎 */
  ttsEngine: TtsEngine
  /** 本地推理设备偏好 */
  computeDevice: ComputeDevice
  /** 语音输入引擎 */
  asrEngine: AsrEngine
  /** 模型下载源 */
  modelSource: ModelSource
  /** 是否在请求里带 safety_check.high；关掉等于让服务端用最低档 */
  sendSafetyCheck: boolean
  /** 采样参数：null 表示不发送，用服务端默认 */
  temperature: number | null
  topP: number | null
  maxOutputTokens: number | null
  /** 角色卡生成的提示词；与 systemPrompt 独立，二者同时生效 */
  characterPrompt: string
  /** 当前角色卡名字，仅用于界面展示 */
  characterName: string
  /** 朗读语速倍数 */
  ttsRate: number
  /** 系统语音的音色名（空 = 自动挑中文语音） */
  ttsSystemVoice: string
  /** 进阶 TTS：按上下文匹配语速与音高 */
  advancedTts: boolean
  /** 是否显示账户余额 */
  showBalance: boolean
  /** 生图（BYOK） */
  imageEnabled: boolean
  imageBaseUrl: string
  imageApiKey: string
  imageModel: string
  /** 生图走云端 BYOK 还是本地 NPU 通道 */
  imageProvider: ImageProvider
}

/** 官方默认系统提示词，与 chat-demo 一致 */
export const DEFAULT_API_BASE_URL = 'https://api.deepseek.com'
export const DEFAULT_SYSTEM_PROMPT = '该助手为DeepSeek，由深度求索公司创造。'
export const DEFAULT_SKIN = 'deepseek'
export const DEFAULT_IMAGE_BASE_URL = 'https://api.openai.com/v1'
export const DEFAULT_IMAGE_MODEL = 'gpt-image-1'

const KEYS = {
  apiKey: 'ods:api-key',
  locale: 'ods:locale',
  location: 'ods:location',
  themePreference: 'ods:theme-preference',
  ttsVoice: 'ods:tts-voice',
  thinking: 'ods:thinking',
  search: 'ods:search',
  siderCollapsed: 'ods:sider-collapsed',
  uiMode: 'ods:ui-mode',
  onboarded: 'ods:onboarded',
  apiBaseUrl: 'ods:api-base-url',
  systemPrompt: 'ods:system-prompt',
  skin: 'ods:skin',
  fontScale: 'ods:font-scale',
  ttsEngine: 'ods:tts-engine',
  computeDevice: 'ods:compute-device',
  asrEngine: 'ods:asr-engine',
  modelSource: 'ods:model-source',
  sendSafetyCheck: 'ods:send-safety-check',
  temperature: 'ods:temperature',
  topP: 'ods:top-p',
  maxOutputTokens: 'ods:max-output-tokens',
  imageEnabled: 'ods:image-enabled',
  imageBaseUrl: 'ods:image-base-url',
  imageApiKey: 'ods:image-api-key',
  imageModel: 'ods:image-model',
  imageProvider: 'ods:image-provider',
  characterPrompt: 'ods:character-prompt',
  characterName: 'ods:character-name',
  ttsRate: 'ods:tts-rate',
  ttsSystemVoice: 'ods:tts-system-voice',
  advancedTts: 'ods:advanced-tts',
  showBalance: 'ods:show-balance',
} as const

/** 旧版 chat-demo 的键前缀，首次启动时迁移一次，避免升级后丢 key */
const LEGACY_PREFIX = 'chat-demo:'

const read = (key: string) => {
  try {
    const value = localStorage.getItem(key)
    if (value !== null) {
      return value
    }
    // 一次性迁移官方 demo 的旧设置
    const legacyKey = key.replace('ods:', LEGACY_PREFIX)
    return legacyKey === key ? null : localStorage.getItem(legacyKey)
  } catch {
    return null
  }
}

const write = (key: string, value: string | null) => {
  try {
    if (value === null) {
      localStorage.removeItem(key)
    } else {
      localStorage.setItem(key, value)
    }
  } catch {
    // 存储不可用时只在内存中生效
  }
}

/** 位置选择模式跟随浏览器语言，与应用内选择的界面语言无关。 */
export const isChineseBrowser = (): boolean =>
  (typeof navigator === 'undefined' ? 'zh' : navigator.language).toLowerCase().startsWith('zh')

const initialLocale = (): Locale => {
  const saved = read(KEYS.locale)
  if (saved === 'zh-CN' || saved === 'en-US') {
    return saved
  }
  return isChineseBrowser() ? 'zh-CN' : 'en-US'
}

const initialLocation = (): UserLocation | null => {
  try {
    const location = normalizeLocation(JSON.parse(read(KEYS.location) ?? 'null'))
    if (!location) {
      return null
    }
    return isChineseBrowser()
      ? location.region === 'CN' && location.province
        ? location
        : null
      : { region: location.region }
  } catch {
    return null
  }
}

/** 未保存过时跟随系统 */
const initialThemePreference = (): ThemePreference => {
  const saved = read(KEYS.themePreference)
  return saved === 'light' || saved === 'dark' ? saved : 'system'
}

/** 未保存过时使用服务端默认音色 stella（海星） */
const initialTtsVoice = (): TtsVoice => (read(KEYS.ttsVoice) === 'tide' ? 'tide' : 'stella')

const initialUiMode = (): UiMode => (read(KEYS.uiMode) === 'plus' ? 'plus' : 'lite')

const initialTtsRate = (): number => {
  const saved = Number(read(KEYS.ttsRate))
  return Number.isFinite(saved) && saved >= 0.5 && saved <= 2 ? saved : 1
}

const initialFontScale = (): number => {
  const saved = Number(read(KEYS.fontScale))
  if (!Number.isFinite(saved) || saved < 0.8 || saved > 2) {
    return 1
  }
  // 1.15 是老版本给 Lite 的默认值，会顶到屏幕边缘，统一收敛到 1.08
  return saved === 1.15 ? 1.08 : saved
}

const initialTtsEngine = (): TtsEngine => {
  const saved = read(KEYS.ttsEngine)
  return saved === 'kokoro' || saved === 'cloud' ? saved : 'system'
}

const initialComputeDevice = (): ComputeDevice => {
  const saved = read(KEYS.computeDevice)
  return saved === 'npu' || saved === 'gpu' || saved === 'cpu' ? saved : 'auto'
}

const initialAsrEngine = (): AsrEngine => {
  const saved = read(KEYS.asrEngine)
  return saved === 'local' || saved === 'cloud' ? saved : 'system'
}

/** 读一个可空的数字设置；空字符串或非法值返回 null（= 不发送该参数） */
const initialNumber = (key: string): number | null => {
  const raw = read(key)
  if (raw === null || raw.trim() === '') {
    return null
  }
  const value = Number(raw)
  return Number.isFinite(value) ? value : null
}

const initialModelSource = (): ModelSource => {
  const saved = read(KEYS.modelSource)
  return saved === 'huggingface' || saved === 'kaggle' || saved === 'manual' ? saved : 'hf-mirror'
}

const initialApiBaseUrl = (): string => {
  const saved = read(KEYS.apiBaseUrl)?.trim()
  return saved ? saved.replace(/\/+$/, '') : DEFAULT_API_BASE_URL
}

export const useSettings = create<Settings>(() => ({
  apiKey: read(KEYS.apiKey),
  locale: initialLocale(),
  location: initialLocation(),
  themePreference: initialThemePreference(),
  ttsVoice: initialTtsVoice(),
  // Lite 没手动设过时默认打开深度思考（长辈问复杂问题更靠谱）
  thinking:
    read(KEYS.thinking) === 'true' ||
    (read(KEYS.thinking) === null && initialUiMode() === 'lite'),
  search: read(KEYS.search) === 'true',
  siderCollapsed: read(KEYS.siderCollapsed) === 'true',
  uiMode: initialUiMode(),
  onboarded: read(KEYS.onboarded) === 'true',
  apiBaseUrl: initialApiBaseUrl(),
  systemPrompt: read(KEYS.systemPrompt) ?? '',
  skin: read(KEYS.skin) ?? DEFAULT_SKIN,
  fontScale: initialFontScale(),
  ttsEngine: initialTtsEngine(),
  computeDevice: initialComputeDevice(),
  asrEngine: initialAsrEngine(),
  modelSource: initialModelSource(),
  sendSafetyCheck: read(KEYS.sendSafetyCheck) === 'true',
  temperature: initialNumber(KEYS.temperature),
  topP: initialNumber(KEYS.topP),
  maxOutputTokens: initialNumber(KEYS.maxOutputTokens),
  imageEnabled: read(KEYS.imageEnabled) === 'true',
  imageBaseUrl: read(KEYS.imageBaseUrl) ?? DEFAULT_IMAGE_BASE_URL,
  imageApiKey: read(KEYS.imageApiKey) ?? '',
    imageModel: read(KEYS.imageModel) ?? DEFAULT_IMAGE_MODEL,
  imageProvider: read(KEYS.imageProvider) === 'local' ? 'local' : 'cloud',
  characterPrompt: read(KEYS.characterPrompt) ?? '',
  characterName: read(KEYS.characterName) ?? '',
  ttsRate: initialTtsRate(),
  ttsSystemVoice: read(KEYS.ttsSystemVoice) ?? '',
  advancedTts: read(KEYS.advancedTts) === 'true',
  showBalance: read(KEYS.showBalance) !== '0',
}))

export const setLocale = (locale: Locale) => {
  write(KEYS.locale, locale)
  useSettings.setState({ locale })
}

export const setLocation = (value: UserLocation | null) => {
  const location = normalizeLocation(value)
  write(KEYS.location, location ? JSON.stringify(location) : null)
  useSettings.setState({ location })
}

export const setThemePreference = (themePreference: ThemePreference) => {
  write(KEYS.themePreference, themePreference)
  useSettings.setState({ themePreference })
}

export const setTtsVoice = (ttsVoice: TtsVoice) => {
  write(KEYS.ttsVoice, ttsVoice)
  useSettings.setState({ ttsVoice })
}

export const setApiKey = (apiKey: string | null) => {
  write(KEYS.apiKey, apiKey)
  useSettings.setState({ apiKey })
}

export const setThinking = (thinking: boolean) => {
  write(KEYS.thinking, String(thinking))
  useSettings.setState({ thinking })
}

export const setSearch = (search: boolean) => {
  write(KEYS.search, String(search))
  useSettings.setState({ search })
}

export const setSiderCollapsed = (siderCollapsed: boolean) => {
  write(KEYS.siderCollapsed, String(siderCollapsed))
  useSettings.setState({ siderCollapsed })
}

export const setUiMode = (uiMode: UiMode) => {
  // Lite 面向长辈：默认打开深度思考，回答更靠谱
  if (uiMode === 'lite' && !useSettings.getState().thinking) {
    setThinking(true)
  }
  write(KEYS.uiMode, uiMode)
  // lite 模式默认放大字号，切回 plus 时回到 1
  write(KEYS.fontScale, uiMode === 'lite' ? '1.08' : '1')
  useSettings.setState({ uiMode, fontScale: uiMode === 'lite' ? 1.08 : 1 })
}

export const completeOnboarding = (uiMode: UiMode) => {
  write(KEYS.onboarded, 'true')
  useSettings.setState({ onboarded: true })
  setUiMode(uiMode)
}

export const setApiBaseUrl = (apiBaseUrl: string) => {
  const normalized = apiBaseUrl.trim().replace(/\/+$/, '') || DEFAULT_API_BASE_URL
  write(KEYS.apiBaseUrl, normalized)
  useSettings.setState({ apiBaseUrl: normalized })
}

export const setCharacterPrompt = (characterPrompt: string, characterName = '') => {
  write(KEYS.characterPrompt, characterPrompt)
  write(KEYS.characterName, characterName)
  useSettings.setState({ characterPrompt, characterName })
}

export const setTtsRate = (ttsRate: number) => {
  const clamped = Math.min(2, Math.max(0.5, Math.round(ttsRate * 10) / 10))
  write(KEYS.ttsRate, String(clamped))
  useSettings.setState({ ttsRate: clamped })
}

export const setTtsSystemVoice = (ttsSystemVoice: string) => {
  write(KEYS.ttsSystemVoice, ttsSystemVoice || null)
  useSettings.setState({ ttsSystemVoice })
}

export const setAdvancedTts = (advancedTts: boolean) => {
  write(KEYS.advancedTts, String(advancedTts))
  useSettings.setState({ advancedTts })
}

export const setShowBalance = (showBalance: boolean) => {
  write(KEYS.showBalance, showBalance ? '1' : '0')
  useSettings.setState({ showBalance })
}

export const setSystemPrompt = (systemPrompt: string) => {
  write(KEYS.systemPrompt, systemPrompt)
  useSettings.setState({ systemPrompt })
}

export const setSkin = (skin: string) => {
  write(KEYS.skin, skin)
  useSettings.setState({ skin })
}

export const setFontScale = (fontScale: number) => {
  const clamped = Math.min(2, Math.max(0.8, Math.round(fontScale * 100) / 100))
  write(KEYS.fontScale, String(clamped))
  useSettings.setState({ fontScale: clamped })
}

export const setTtsEngine = (ttsEngine: TtsEngine) => {
  write(KEYS.ttsEngine, ttsEngine)
  useSettings.setState({ ttsEngine })
}

export const setComputeDevice = (computeDevice: ComputeDevice) => {
  write(KEYS.computeDevice, computeDevice)
  useSettings.setState({ computeDevice })
}

export const setAsrEngine = (asrEngine: AsrEngine) => {
  write(KEYS.asrEngine, asrEngine)
  useSettings.setState({ asrEngine })
}

export const setModelSource = (modelSource: ModelSource) => {
  write(KEYS.modelSource, modelSource)
  useSettings.setState({ modelSource })
}

export const setSendSafetyCheck = (sendSafetyCheck: boolean) => {
  write(KEYS.sendSafetyCheck, String(sendSafetyCheck))
  useSettings.setState({ sendSafetyCheck })
}

/** 采样参数写 null 等于恢复服务端默认 */
export const setSamplingParam = (
  key: 'temperature' | 'topP' | 'maxOutputTokens',
  value: number | null
) => {
  const storageKey =
    key === 'temperature' ? KEYS.temperature : key === 'topP' ? KEYS.topP : KEYS.maxOutputTokens
  write(storageKey, value === null ? null : String(value))
  useSettings.setState({ [key]: value } as never)
}

export const setImageEnabled = (imageEnabled: boolean) => {
  write(KEYS.imageEnabled, String(imageEnabled))
  useSettings.setState({ imageEnabled })
}

export const setImageBaseUrl = (imageBaseUrl: string) => {
  write(KEYS.imageBaseUrl, imageBaseUrl.trim())
  useSettings.setState({ imageBaseUrl: imageBaseUrl.trim() })
}

export const setImageApiKey = (imageApiKey: string) => {
  write(KEYS.imageApiKey, imageApiKey)
  useSettings.setState({ imageApiKey })
}

export const setImageProvider = (imageProvider: ImageProvider) => {
  write(KEYS.imageProvider, imageProvider)
  useSettings.setState({ imageProvider })
}

export const setImageModel = (imageModel: string) => {
  write(KEYS.imageModel, imageModel)
  useSettings.setState({ imageModel })
}

/**
 * 当前生效的系统提示词。
 * 系统提示词优先：填了系统提示词就只用它（角色卡不参与，避免两套设定打架）；
 * 系统提示词为空时才用角色卡；两者都空回落官方默认。
 */
export const resolveSystemPrompt = (): string => {
  const { systemPrompt, characterPrompt } = useSettings.getState()
  const global = systemPrompt.trim()
  if (global) {
    return global
  }
  const card = characterPrompt.trim()
  return card || DEFAULT_SYSTEM_PROMPT
}
