import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

zh = [
    ("odsModels", "本地模型"),
    ("odsModelsHint", "当前下载源：{source}；下载后缓存在设备上，可离线使用"),
    ("odsModelDownload", "下载"),
    ("odsModelResume", "继续下载"),
    ("odsModelDelete", "删除"),
    ("odsModelReady", "已就绪"),
    ("odsModelPartial", "部分文件缺失，可继续下载"),
    ("odsModelMissing", "未下载（共 {size}）"),
    ("odsModelDownloading", "下载中 {percent}%"),
]
en = [
    ("odsModels", "Local models"),
    ("odsModelsHint", "Download source: {source}. Files are cached on the device and work offline"),
    ("odsModelDownload", "Download"),
    ("odsModelResume", "Resume"),
    ("odsModelDelete", "Delete"),
    ("odsModelReady", "Ready"),
    ("odsModelPartial", "Some files are missing"),
    ("odsModelMissing", "Not downloaded ({size})"),
    ("odsModelDownloading", "Downloading {percent}%"),
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

# ExtSettings: 插入模型管理
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { SettingCell } from './SettingCell.js'",
    "import { SettingCell } from './SettingCell.js'\nimport { ModelsSection } from './ModelsSection.js'",
    1,
)
old = """    <AppearanceSettings />
    <VoiceSettings />
    <ImageSettings />"""
new = """    <AppearanceSettings />
    <VoiceSettings />
    <ModelsSection />
    <ImageSettings />"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched ExtSettings.tsx")
