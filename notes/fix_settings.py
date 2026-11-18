import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()

# 1) 类型字段
old = """  /** 生图（BYOK） */
  imageEnabled: boolean"""
new = """  /** 角色卡生成的提示词；与 systemPrompt 独立，二者同时生效 */
  characterPrompt: string
  /** 当前角色卡名字，仅用于界面展示 */
  characterName: string
  /** 朗读语速倍数 */
  ttsRate: number
  /** 系统语音的音色名（空 = 自动挑中文语音） */
  ttsSystemVoice: string
  /** 是否显示账户余额 */
  showBalance: boolean
  /** 生图（BYOK） */
  imageEnabled: boolean"""
assert old in t
t = t.replace(old, new, 1)

# 2) 键
old = """  imageModel: 'ods:image-model',
} as const"""
new = """  imageModel: 'ods:image-model',
  characterPrompt: 'ods:character-prompt',
  characterName: 'ods:character-name',
  ttsRate: 'ods:tts-rate',
  ttsSystemVoice: 'ods:tts-system-voice',
  showBalance: 'ods:show-balance',
} as const"""
assert old in t
t = t.replace(old, new, 1)

# 3) 初始值
old = """  imageModel: read(KEYS.imageModel) ?? DEFAULT_IMAGE_MODEL,"""
new = """    imageModel: read(KEYS.imageModel) ?? DEFAULT_IMAGE_MODEL,
  characterPrompt: read(KEYS.characterPrompt) ?? '',
  characterName: read(KEYS.characterName) ?? '',
  ttsRate: initialTtsRate(),
  ttsSystemVoice: read(KEYS.ttsSystemVoice) ?? '',
  showBalance: read(KEYS.showBalance) !== '0',"""
assert old in t
t = t.replace(old, new, 1)

# 4) 语速解析函数（放在 initialTtsVoice 之后）
old = """const initialFontScale = (): number => {"""
new = """const initialTtsRate = (): number => {
  const saved = Number(read(KEYS.ttsRate))
  return Number.isFinite(saved) && saved >= 0.5 && saved <= 2 ? saved : 1
}

const initialFontScale = (): number => {"""
assert old in t
t = t.replace(old, new, 1)

# 5) setter + resolveSystemPrompt 重写
old = """export const setSystemPrompt = (systemPrompt: string) => {"""
new = """export const setCharacterPrompt = (characterPrompt: string, characterName = '') => {
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

export const setShowBalance = (showBalance: boolean) => {
  write(KEYS.showBalance, showBalance ? '1' : '0')
  useSettings.setState({ showBalance })
}

export const setSystemPrompt = (systemPrompt: string) => {"""
assert old in t
t = t.replace(old, new, 1)

old = """/** 当前生效的系统提示词：自定义为空时回落官方默认 */
export const resolveSystemPrompt = (): string => {
  const custom = useSettings.getState().systemPrompt.trim()
  return custom || DEFAULT_SYSTEM_PROMPT
}"""
new = """/**
 * 当前生效的系统提示词。
 * 全局提示词与角色卡各自独立，同时存在时按「全局 → 角色卡」拼接；都为空才回落官方默认。
 */
export const resolveSystemPrompt = (): string => {
  const { systemPrompt, characterPrompt } = useSettings.getState()
  const parts = [systemPrompt.trim(), characterPrompt.trim()].filter(Boolean)
  return parts.length > 0 ? parts.join('\\n\\n') : DEFAULT_SYSTEM_PROMPT
}"""
assert old in t
t = t.replace(old, new, 1)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settings.ts patched")
