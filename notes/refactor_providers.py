import io
import pathlib
import re

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()

new_block = '''/**
 * 供应商：一套「服务地址 + Key」，下面挂多个可选模型。
 * DeepSeek 官方、OpenAI、硅基流动、OpenRouter、自建中转都按这个结构算。
 */
export type Provider = {
  id: string
  name: string
  baseUrl: string
  /** 留空表示沿用全局 API Key */
  apiKey?: string
  /** 该供应商可选的模型名 */
  models: string[]
}

/** 内置供应商 */
export const BUILTIN_PROVIDERS: Provider[] = [
  {
    id: 'deepseek',
    name: 'DeepSeek 官方',
    baseUrl: 'https://api.deepseek.com',
    models: ['deepseek-v4.1-flash', 'deepseek-v4-pro'],
  },
  {
    id: 'openai',
    name: 'OpenAI',
    baseUrl: 'https://api.openai.com/v1',
    models: ['gpt-4o-mini', 'gpt-4o'],
  },
  {
    id: 'custom',
    name: '自定义（OpenAI 兼容）',
    baseUrl: '',
    models: [],
  },
]

const readProviders = (): Provider[] => {
  const raw = read(KEYS.providers)
  if (!raw) {
    return BUILTIN_PROVIDERS
  }
  try {
    const parsed = JSON.parse(raw) as Provider[]
    return Array.isArray(parsed) && parsed.length > 0 ? parsed : BUILTIN_PROVIDERS
  } catch {
    return BUILTIN_PROVIDERS
  }
}
'''

# 替换掉旧的 ProviderPreset 定义
start = t.find('/**\n * 模型方案：一套「服务地址 + Key + 模型名」的组合。')
end = t.find("export type Locale = 'zh-CN' | 'en-US'")
assert start >= 0 and end > start
t = t[:start] + new_block + t[end:]

# 状态字段
t = t.replace(
    "  /** 模型方案列表（服务地址 + Key + 模型名） */\n  presets: ProviderPreset[]\n  /** 当前使用的方案 id */\n  activePreset: string",
    "  /** 供应商列表 */\n  providers: Provider[]\n  /** 当前供应商 id */\n  activeProvider: string",
    1,
)
t = t.replace(
    "  presets: readPresets(),\n  activePreset: read(KEYS.activePreset) ?? 'deepseek',",
    "  providers: readProviders(),\n  activeProvider: read(KEYS.activeProvider) ?? 'deepseek',",
    1,
)
t = t.replace(
    "  presets: 'ods:presets',\n  activePreset: 'ods:active-preset',",
    "  providers: 'ods:providers',\n  activeProvider: 'ods:active-provider',",
    1,
)

# setters
old_start = t.find("/** 切换模型方案：把方案里的地址/模型/Key 写进当前生效设置 */")
old_end = t.find("export const setModel = ")
assert old_start >= 0 and old_end > old_start
new_setters = '''/** 切换到某个供应商：写地址与 Key，模型切到它的第一个 */
export const applyProvider = (id: string) => {
  const state = useSettings.getState()
  const provider = state.providers.find((item) => item.id === id)
  if (!provider) {
    return
  }
  const baseUrl = provider.baseUrl.trim()
  const nextModel = provider.models[0] ?? state.model
  write(KEYS.activeProvider, id)
  if (baseUrl) {
    write(KEYS.apiBaseUrl, baseUrl)
  }
  write(KEYS.model, nextModel)
  if (provider.apiKey) {
    write(KEYS.apiKey, provider.apiKey)
  }
  useSettings.setState({
    activeProvider: id,
    ...(baseUrl ? { apiBaseUrl: baseUrl } : {}),
    model: nextModel,
    ...(provider.apiKey ? { apiKey: provider.apiKey } : {}),
  })
}

const persistProviders = (providers: Provider[]) => {
  write(KEYS.providers, JSON.stringify(providers))
  useSettings.setState({ providers })
}

/** 新增或更新一个供应商 */
export const saveProvider = (provider: Provider) => {
  const list = useSettings.getState().providers
  const exists = list.some((item) => item.id === provider.id)
  persistProviders(
    exists ? list.map((item) => (item.id === provider.id ? provider : item)) : [...list, provider]
  )
}

export const removeProvider = (id: string) => {
  persistProviders(useSettings.getState().providers.filter((item) => item.id !== id))
}

'''
t = t[:old_start] + new_setters + t[old_end:]

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settings providers ok")
