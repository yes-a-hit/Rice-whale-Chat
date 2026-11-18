import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- system.ts 接入进阶 TTS ----------
p = root / "src/services/speech/engines/system.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { useSettings } from '../../settings.js'",
    "import { useSettings } from '../../settings.js'\nimport { matchVoiceProfile, stripUnreadable } from '../contextVoice.js'",
    1,
)

old = """const speakOne = (text: string, voice: SpeechSynthesisVoice | undefined) =>
  new Promise<void>((resolve, reject) => {
    const utterance = new SpeechSynthesisUtterance(text)
    if (voice) {
      utterance.voice = voice
      utterance.lang = voice.lang
    }
    utterance.rate = useSettings.getState().ttsRate
    utterance.pitch = 1"""
new = """type SpeakTuning = { rate: number; pitch: number }

const speakOne = (text: string, voice: SpeechSynthesisVoice | undefined, tuning: SpeakTuning) =>
  new Promise<void>((resolve, reject) => {
    const utterance = new SpeechSynthesisUtterance(text)
    if (voice) {
      utterance.voice = voice
      utterance.lang = voice.lang
    }
    utterance.rate = tuning.rate
    utterance.pitch = tuning.pitch"""
assert old in t
t = t.replace(old, new, 1)

old2 = """    const chunks = splitSentences(text)
    if (chunks.length === 0) {
      return
    }
    const voice = pickVoice()"""
new2 = """    const { ttsRate, advancedTts } = useSettings.getState()
    // 进阶 TTS：按上下文挑语速/音高，并把代码、表格、链接换成口播话术
    const spoken = advancedTts ? stripUnreadable(text) : text
    const profile = advancedTts ? matchVoiceProfile(spoken, ttsRate) : null
    const tuning: SpeakTuning = { rate: profile?.rate ?? ttsRate, pitch: profile?.pitch ?? 1 }
    const chunks = splitSentences(spoken)
    if (chunks.length === 0) {
      return
    }
    const voice = pickVoice()"""
assert old2 in t
t = t.replace(old2, new2, 1)

t = t.replace("      await speakOne(chunk, voice)", "      await speakOne(chunk, voice, tuning)", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("system tts ok")

# ---------- settings：advancedTts 字段 ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
if "advancedTts" not in t:
    t = t.replace(
        "  ttsSystemVoice: string",
        "  ttsSystemVoice: string\n  /** 进阶 TTS：按上下文匹配语速与音高 */\n  advancedTts: boolean",
        1,
    )
    t = t.replace(
        "  ttsSystemVoice: 'ods:tts-system-voice',",
        "  ttsSystemVoice: 'ods:tts-system-voice',\n  advancedTts: 'ods:advanced-tts',",
        1,
    )
    t = t.replace(
        "  ttsSystemVoice: read(KEYS.ttsSystemVoice) ?? '',",
        "  ttsSystemVoice: read(KEYS.ttsSystemVoice) ?? '',\n  advancedTts: read(KEYS.advancedTts) === 'true',",
        1,
    )
    t = t.replace(
        "export const setShowBalance =",
        """export const setAdvancedTts = (advancedTts: boolean) => {
  write(KEYS.advancedTts, String(advancedTts))
  useSettings.setState({ advancedTts })
}

export const setShowBalance =""",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settings advancedTts ok")
