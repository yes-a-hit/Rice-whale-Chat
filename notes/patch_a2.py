import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- store.ts: 系统提示词改为可配置 ----------
p = root / "src/services/chat/store.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { useSettings } from '../settings.js'",
    "import { resolveSystemPrompt, useSettings } from '../settings.js'",
)
old = "const SYSTEM_PROMPT = '该助手为DeepSeek，由深度求索公司创造。'"
assert old in t
t = t.replace(old, "/** 系统提示词由设置决定：留空时回落到官方默认（Plus 模式可覆盖） */")
t = t.replace("system: SYSTEM_PROMPT,", "system: resolveSystemPrompt(),")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched store.ts")

# ---------- settingsDialogState.ts: 新增扩展分组 ----------
p = root / "src/components/settings/settingsDialogState.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "/** 设置弹窗的分组：通用设置 / 数据管理 */\nexport type SettingsSection = 'general' | 'data'",
    "/** 设置弹窗的分组：通用设置 / 扩展 / 数据管理 */\nexport type SettingsSection = 'general' | 'ext' | 'data'",
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched settingsDialogState.ts")
