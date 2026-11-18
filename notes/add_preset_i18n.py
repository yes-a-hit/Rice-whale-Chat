import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

pairs_zh = [
    ("odsPresets", "模型方案"),
    ("odsPresetsHint", "一套「地址 + Key + 模型名」。支持 DeepSeek 官方、OpenAI 以及任何 OpenAI 兼容的中转/自建服务；Key 留空则用上面的通用 Key"),
    ("odsPresetDefaultHost", "默认地址"),
    ("odsPresetName", "方案名称"),
    ("odsPresetBaseUrl", "服务地址，如 https://api.openai.com/v1"),
    ("odsPresetModel", "模型名，如 gpt-4o-mini"),
    ("odsPresetKey", "这个方案专用的 Key（可留空）"),
    ("odsPresetAdd", "＋ 新增方案"),
]
pairs_en = [
    ("odsPresets", "Model presets"),
    ("odsPresetsHint", "A base URL, key and model name. Works with DeepSeek, OpenAI and any OpenAI-compatible gateway; leave the key empty to reuse the global one"),
    ("odsPresetDefaultHost", "default host"),
    ("odsPresetName", "Preset name"),
    ("odsPresetBaseUrl", "Base URL, e.g. https://api.openai.com/v1"),
    ("odsPresetModel", "Model, e.g. gpt-4o-mini"),
    ("odsPresetKey", "Key for this preset (optional)"),
    ("odsPresetAdd", "+ Add preset"),
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
