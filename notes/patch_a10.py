import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# CSS: 隐藏的 file input
p = root / "src/components/settings/Ext.module.css"
t = io.open(p, encoding="utf-8").read()
if ".hiddenFile" not in t:
    t += """
.hiddenFile {
  display: none;
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("css ok")

zh = [
    ("odsCard", "角色卡"),
    ("odsCardHint", "导入 PNG 或 JSON 角色卡（chara card v2），会写入系统提示词"),
    ("odsCardImport", "导入角色卡"),
    ("odsCardImporting", "解析中"),
    ("odsCardClear", "清除"),
    ("odsCardCurrent", "当前角色：{text}"),
    ("odsCardImported", "已导入角色卡「{name}」"),
    ("odsCardImportFailed", "角色卡解析失败：{message}"),
]
en = [
    ("odsCard", "Character card"),
    ("odsCardHint", "Import a PNG or JSON character card (chara card v2); it becomes the system prompt"),
    ("odsCardImport", "Import card"),
    ("odsCardImporting", "Parsing"),
    ("odsCardClear", "Clear"),
    ("odsCardCurrent", "Current character: {text}"),
    ("odsCardImported", "Imported card \"{name}\""),
    ("odsCardImportFailed", "Failed to parse card: {message}"),
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

# ExtSettings: 接入角色卡
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { ModelsSection } from './ModelsSection.js'",
    "import { ModelsSection } from './ModelsSection.js'\nimport { CharacterCardSetting } from './CharacterCardSetting.js'",
    1,
)
old = """    <ApiBaseUrlSetting />
    <SystemPromptSetting />"""
new = """    <ApiBaseUrlSetting />
    <SystemPromptSetting />
    <CharacterCardSetting />"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched ExtSettings.tsx")
