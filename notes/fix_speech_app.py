import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- system 引擎：音色与语速跟随设置 ----------
p = root / "src/services/speech/engines/system.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import type { SpeakContext, TtsEngine } from './types.js'",
    "import { useSettings } from '../../settings.js'\nimport type { SpeakContext, TtsEngine } from './types.js'",
    1,
)
old = """const pickVoice = (): SpeechSynthesisVoice | undefined => {
  const voices = window.speechSynthesis?.getVoices?.() ?? []
  const zh = voices.filter((voice) => voice.lang.toLowerCase().startsWith('zh'))
  // 优先本地（离线）中文语音，其次任意中文，最后系统默认
  return zh.find((voice) => voice.localService) ?? zh[0] ?? voices[0]
}"""
new = """const pickVoice = (): SpeechSynthesisVoice | undefined => {
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
}"""
assert old in t
t = t.replace(old, new, 1)

old = """    utterance.rate = 1
    utterance.pitch = 1"""
new = """    utterance.rate = useSettings.getState().ttsRate
    utterance.pitch = 1"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("system engine ok")

# ---------- App: Lite 自动朗读 + 首启不弹设置 ----------
p = root / "src/app/App.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { stopReadAloud } from '../services/speech/readAloud.js'",
    "import {\n  describeReadAloudError,\n  stopReadAloud,\n  toggleReadAloud,\n} from '../services/speech/readAloud.js'\n"
    "import { onReplyDone } from '../services/chat/replyEvents.js'\n"
    "import { getReplyText } from '../services/chat/reply.js'",
    1,
)
old = """  useEffect(() => {
    void initChat()
    // 首次打开先在设置里输入 API Key
    ensureApiKey()
  }, [])"""
new = """  useEffect(() => {
    void initChat()
  }, [])

  // 选完模式、或已有配置但还没填 Key 时，才引导去设置
  useEffect(() => {
    if (onboarded) {
      ensureApiKey()
    }
  }, [onboarded])

  // Lite 模式：回复完成后自动朗读，长辈不用去找小喇叭按钮
  useEffect(
    () =>
      onReplyDone((sessionId, messageId) => {
        if (useSettings.getState().uiMode !== 'lite') {
          return
        }
        const state = useChatStore.getState()
        if (state.activeId !== sessionId) {
          return
        }
        const message = state.sessionCache[sessionId]?.messages.find((item) => item.id === messageId)
        if (!message || message.role !== 'assistant') {
          return
        }
        const text = getReplyText(message)
        if (text.trim()) {
          toggleReadAloud(messageId, text, (error) => showToast(describeReadAloudError(error)))
        }
      }),
    []
  )"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("App ok")
