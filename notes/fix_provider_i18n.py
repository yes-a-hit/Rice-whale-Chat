import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# setModel 导入
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "  setCollapseThinking,",
    "  setCollapseThinking,\n  setModel,",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("setModel import ok")

# i18n
pairs_zh = [
    ("odsProviders", "供应商与模型"),
    ("odsProvidersHint", "一个供应商是一套「地址 + Key」，下面挂多个模型。DeepSeek、OpenAI、硅基流动、OpenRouter、自建中转都这么配；Key 留空则用上面的通用 Key"),
    ("odsProviderModels", "模型列表，一行一个"),
]
pairs_en = [
    ("odsProviders", "Providers & models"),
    ("odsProvidersHint", "A provider is one base URL + key with several models. Works for DeepSeek, OpenAI, OpenRouter, self-hosted gateways; leave the key empty to reuse the global one"),
    ("odsProviderModels", "Models, one per line"),
]
for path, pairs in (("src/i18n/zh.ts", pairs_zh), ("src/i18n/en.ts", pairs_en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    missing = [f"  {k}: '{v}',\n" for k, v in pairs if f"{k}:" not in t]
    if missing:
        t = t.replace(tail, "".join(missing) + tail, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("i18n", path)
