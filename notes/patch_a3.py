import io, re, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\settings\SettingsDialog.tsx")
t = io.open(p, encoding="utf-8").read()

# 1) import ExtSettings + SettingCell + IconEditOutline16
t = t.replace(
    "  IconDarkOutline16,\n  IconDataOutline16,",
    "  IconDarkOutline16,\n  IconDataOutline16,\n  IconEditOutline16,",
    1,
)
t = t.replace(
    "import { ApiKeyConfirm, ApiKeyField, useApiKeyEditor } from './ApiKeyField.js'",
    "import { ApiKeyConfirm, ApiKeyField, useApiKeyEditor } from './ApiKeyField.js'\n"
    "import { ExtSettings } from './ExtSettings.js'\n"
    "import { errorStatus, SettingCell, type Status } from './SettingCell.js'",
    1,
)

# 2) sections 增加扩展分组
old_sections = """  { value: 'data', label: 'settingDialogAsideDataOptionLabel', icon: <IconDataOutline16 /> },
]"""
new_sections = """  { value: 'ext', label: 'odsExtSection', icon: <IconEditOutline16 /> },
  { value: 'data', label: 'settingDialogAsideDataOptionLabel', icon: <IconDataOutline16 /> },
]"""
assert old_sections in t
t = t.replace(old_sections, new_sections, 1)

# 3) 三分支渲染
old_render = """          {section === 'general' ? (
            <>
              <ThemeSetting />
              <LocaleSetting />
              <TtsVoiceSetting />
              <LocationSetting />
            </>
          ) : ("""
new_render = """          {section === 'ext' ? (
            <ExtSettings />
          ) : section === 'general' ? (
            <>
              <ThemeSetting />
              <LocaleSetting />
              <TtsVoiceSetting />
              <LocationSetting />
            </>
          ) : ("""
assert old_render in t
t = t.replace(old_render, new_render, 1)

# 4) 删除本地 SettingCell / Status / errorStatus 定义（已抽到 SettingCell.tsx）
start = t.index("/** `reason` 为失败原因的文案 key")
end = t.index("/** 选文件后先提示覆盖；确认后才检查文件并执行导入，任何错误都提示导入失败。 */")
removed = t[start:end]
assert "const SettingCell = ({" in removed and "errorStatus" in removed
t = t[:start] + t[end:]

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched SettingsDialog.tsx, removed", len(removed), "chars")
