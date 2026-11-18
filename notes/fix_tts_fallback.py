import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- kokoro：注释写清事实，未就绪时明确报错 ----------
p = root / "src/services/speech/engines/kokoro.ts"
io.open(p, "w", encoding="utf-8", newline="\n").write(
    """import type { SpeakContext, TtsEngine } from './types.js'

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
"""
)
print("kokoro ok")

# ---------- readAloud：本地引擎不可用时自动回落 ----------
p = root / "src/services/speech/readAloud.ts"
t = io.open(p, encoding="utf-8").read()

old = """  const controller = new AbortController()
  current = { controller }
  const engineId = useSettings.getState().ttsEngine
  useReadAloud.setState({ messageId, status: 'loading', engine: engineId })
  const engine = engineFor(engineId)"""
new = """  const controller = new AbortController()
  current = { controller }
  const configured = useSettings.getState().ttsEngine
  // 本地模型引擎没接运行时之前必然不可用，直接回落系统朗读，不让用户点了没反应
  const engineId = configured === 'kokoro' ? 'system' : configured
  if (engineId !== configured) {
    onError(new Error('LOCAL_TTS_FALLBACK'))
  }
  useReadAloud.setState({ messageId, status: 'loading', engine: engineId })
  const engine = engineFor(engineId)"""
assert old in t
t = t.replace(old, new, 1)

old2 = """  if (error instanceof Error && error.message === 'LOCAL_TTS_NOT_INSTALLED') {
    return { key: 'odsLocalTtsMissing' }
  }"""
new2 = """  if (
    error instanceof Error &&
    (error.message === 'LOCAL_TTS_NOT_INSTALLED' || error.message === 'LOCAL_TTS_FALLBACK')
  ) {
    return { key: 'odsLocalTtsFallback' }
  }"""
assert old2 in t
t = t.replace(old2, new2, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("readAloud ok")

# ---------- i18n：回退提示 ----------
for path, value in (
    ("src/i18n/zh.ts", "本地语音引擎还没接好，已改用系统朗读"),
    ("src/i18n/en.ts", "Local voice engine is not ready yet, switched to system speech"),
):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    if "odsLocalTtsFallback" in t:
        continue
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    t = t.replace(tail, f"  odsLocalTtsFallback: '{value}',\n" + tail, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("i18n", path)
