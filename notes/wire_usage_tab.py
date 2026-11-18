import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 状态：新增 usage 分组 ----------
p = root / "src/components/settings/settingsDialogState.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "export type SettingsSection = 'general' | 'ext' | 'data'",
    "export type SettingsSection = 'general' | 'ext' | 'usage' | 'data'",
)
t = t.replace(
    "return value === 'ext' || value === 'data' || value === 'general' ? value : 'general'",
    "return value === 'ext' || value === 'data' || value === 'usage' || value === 'general'\n    ? value\n    : 'general'",
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("state ok")

# ---------- 2. 侧栏加「用量」，并渲染 UsageSection ----------
p = root / "src/components/settings/SettingsDialog.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "    { value: 'data', label: 'settingDialogAsideDataOptionLabel', icon: <IconDataOutline16 /> },",
    "    { value: 'usage', label: 'odsUsageSection', icon: <IconDataOutline16 /> },\n"
    "    { value: 'data', label: 'settingDialogAsideDataOptionLabel', icon: <IconDataOutline16 /> },",
    1,
)
t = t.replace(
    """          {section === 'ext' ? (
            <ExtSettings />
          ) : section === 'general' ? (""",
    """          {section === 'ext' ? (
            <ExtSettings />
          ) : section === 'usage' ? (
            <UsageSection />
          ) : section === 'general' ? (""",
    1,
)
t = t.replace(
    "import { ExtSettings } from './ExtSettings.js'",
    "import { ExtSettings } from './ExtSettings.js'\nimport { UsageSection } from './UsageSection.js'",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("dialog ok")

# ---------- 3. 无 API Key 时用 hungry 图 ----------
p = root / "src/components/session/Welcome.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace('/media/no-key.png', '/media/hungry.png')
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("welcome image ok")
