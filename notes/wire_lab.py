import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

zh = [
    ("odsLabSection", "实验性玩法"),
    ("odsLabTitle", "实验性玩法"),
    ("odsLabHint", "本地模型、NPU 推理、进阶语音。默认全关，开了也不保证跑得起来——出问题不影响日常聊天。"),
    (
        "odsLabTtsHint",
        "本地模型 TTS 需要推理运行时；当前环境会自动回落到系统朗读。真吃 NPU 得等原生插件",
    ),
    ("odsAdvancedTts", "进阶 TTS：按上下文配音"),
    (
        "odsAdvancedTtsHint",
        "问句放慢、感叹句加快、列表多停顿，代码与表格换成口播话术，跳过链接",
    ),
    ("odsLocalImage", "本地生图通道"),
    (
        "odsLocalImageHint",
        "还未接通：0.5B 改写提示词 → CLIP → SD-Turbo 1.5B → VAE → 输出图片",
    ),
    ("odsLocalImageReady", "原生桥已就绪，可走本地管线"),
    ("odsImageCloud", "云端 BYOK"),
    ("odsImageLocal", "本地 NPU"),
]
en = [
    ("odsLabSection", "Lab"),
    ("odsLabTitle", "Experimental"),
    ("odsLabHint", "Local models, NPU inference, advanced speech. Off by default; nothing here can break normal chat."),
    ("odsLabTtsHint", "Local TTS needs a runtime; falls back to system speech until then"),
    ("odsAdvancedTts", "Context-aware voice"),
    ("odsAdvancedTtsHint", "Slower for questions, faster for exclamations, pauses on lists, code and tables are skipped"),
    ("odsLocalImage", "Local image pipeline"),
    ("odsLocalImageHint", "Not wired yet: 0.5B prompt rewrite, CLIP, SD-Turbo, VAE"),
    ("odsLocalImageReady", "Native bridge ready"),
    ("odsImageCloud", "Cloud BYOK"),
    ("odsImageLocal", "Local NPU"),
]

for path, pairs in (("src/i18n/zh.ts", zh), ("src/i18n/en.ts", en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    if pairs[0][0] in t:
        print("skip", path)
        continue
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    block = "".join(f"  {k}: '{v}',\n" for k, v in pairs)
    t = t.replace(tail, block + tail, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("ok", path)

# ---------- 设置加 lab 分组 ----------
p = root / "src/components/settings/settingsDialogState.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "export type SettingsSection = 'general' | 'ext' | 'usage' | 'data'",
    "export type SettingsSection = 'general' | 'ext' | 'usage' | 'lab' | 'data'",
)
t = t.replace(
    "return value === 'ext' || value === 'data' || value === 'usage' || value === 'general'",
    "return value === 'ext' ||\n    value === 'data' ||\n    value === 'usage' ||\n    value === 'lab' ||\n    value === 'general'",
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("section type ok")

p = root / "src/components/settings/SettingsDialog.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "  { value: 'data', label: 'settingDialogAsideDataOptionLabel', icon: <IconDataOutline16 /> },",
    "  { value: 'lab', label: 'odsLabSection', icon: <IconChartOutline16 /> },\n"
    "  { value: 'data', label: 'settingDialogAsideDataOptionLabel', icon: <IconDataOutline16 /> },",
    1,
)
t = t.replace(
    """          ) : section === 'usage' ? (
            <UsageSection />""",
    """          ) : section === 'usage' ? (
            <UsageSection />
          ) : section === 'lab' ? (
            <LabSettings />""",
    1,
)
t = t.replace(
    "import { UsageSection } from './UsageSection.js'",
    "import { UsageSection } from './UsageSection.js'\nimport { LabSettings } from './LabSettings.js'",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("dialog lab ok")
