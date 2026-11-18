import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. settings：模型方案（provider preset） ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()

if "ProviderPreset" not in t:
    t = t.replace(
        "export type Locale = 'zh-CN' | 'en-US'",
        """/**
 * 模型方案：一套「服务地址 + Key + 模型名」的组合。
 * 支持任何 OpenAI 兼容接口（DeepSeek 官方 / OpenAI / 中转站 / 自建）。
 */
export type ProviderPreset = {
  id: string
  name: string
  baseUrl: string
  /** 留空表示沿用全局 API Key */
  apiKey?: string
  model: string
}

/** 内置方案：官方 DeepSeek + OpenAI 兼容入口 */
export const BUILTIN_PRESETS: ProviderPreset[] = [
  { id: 'deepseek', name: 'DeepSeek 官方', baseUrl: 'https://api.deepseek.com', model: 'deepseek-v4.1-flash' },
  { id: 'openai', name: 'OpenAI', baseUrl: 'https://api.openai.com/v1', model: 'gpt-4o-mini' },
  { id: 'custom', name: '自定义（OpenAI 兼容）', baseUrl: '', model: '' },
]

const readPresets = (): ProviderPreset[] => {
  const raw = read(KEYS.presets)
  if (!raw) {
    return BUILTIN_PRESETS
  }
  try {
    const parsed = JSON.parse(raw) as ProviderPreset[]
    return Array.isArray(parsed) && parsed.length > 0 ? parsed : BUILTIN_PRESETS
  } catch {
    return BUILTIN_PRESETS
  }
}

export type Locale = 'zh-CN' | 'en-US'""",
        1,
    )
    t = t.replace(
        "  model: ChatModel",
        "  model: string\n  /** 模型方案列表（服务地址 + Key + 模型名） */\n  presets: ProviderPreset[]\n  /** 当前使用的方案 id */\n  activePreset: string",
        1,
    )
    t = t.replace(
        "  model: initialModel(),",
        "  model: initialModel(),\n  presets: readPresets(),\n  activePreset: read(KEYS.activePreset) ?? 'deepseek',",
        1,
    )
    t = t.replace(
        "  model: 'ods:model',",
        "  model: 'ods:model',\n  presets: 'ods:presets',\n  activePreset: 'ods:active-preset',",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("settings presets ok")
