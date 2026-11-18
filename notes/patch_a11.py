import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

zh = [
    ("odsImageDialogTitle", "AI 生图"),
    ("odsImageGenerate", "生成"),
    ("odsImageGenerating", "生成中…"),
    ("odsImageSave", "保存图片"),
    ("odsImagePromptPlaceholder", "描述你想要的画面"),
    ("odsImageSize", "尺寸"),
    ("odsImageNotConfigured", "还没配置生图服务。在设置里填入服务地址、Key 与模型名即可（BYOK）。"),
    ("odsImageOpenSettings", "去设置"),
]
en = [
    ("odsImageDialogTitle", "Image generation"),
    ("odsImageGenerate", "Generate"),
    ("odsImageGenerating", "Generating…"),
    ("odsImageSave", "Save image"),
    ("odsImagePromptPlaceholder", "Describe the image you want"),
    ("odsImageSize", "Size"),
    ("odsImageNotConfigured", "No image service yet. Add the endpoint, key and model in settings (BYOK)."),
    ("odsImageOpenSettings", "Open settings"),
]

for path, pairs, tail in [
    ("src/i18n/zh.ts", zh, "} as const"),
    ("src/i18n/en.ts", en, "} satisfies Record<keyof typeof zh, string>"),
]:
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    if pairs[0][0] in t:
        print("skip", path)
        continue
    block = "".join(f"  {k}: '{v}',\n" for k, v in pairs)
    t = t.replace(tail, block + tail, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("ok", path)
