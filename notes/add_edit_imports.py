import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

p = root / "src/components/messages/AssistantMessage.tsx"
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    "import { memo } from 'react'",
    "import { memo, useState } from 'react'",
    1,
)
t = t.replace(
    "import { IconRefreshOutline16, IconWarningOutline16 } from '../base/icons.js'",
    "import {\n  IconEditOutline16,\n  IconRefreshOutline16,\n  IconTrashOutline16,\n  IconWarningOutline16,\n} from '../base/icons.js'",
    1,
)
t = t.replace(
    "import { continueReply, regenerateReply } from '../../services/chat/store.js'",
    "import { continueReply, deleteMessage, editReply, regenerateReply } from '../../services/chat/store.js'",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("imports ok")

# 编辑器样式
p = root / "src/components/messages/AssistantMessage.module.css"
t = io.open(p, encoding="utf-8").read()
if ".editor" not in t:
    t += """
.editor {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 4px 0 8px;
}

.editorInput {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border: 1px solid var(--dsw-alias-border-l2);
  border-radius: 12px;
  background: var(--dsw-alias-bg-base);
  color: var(--dsw-alias-label-primary);
  font: inherit;
  font-size: 14.5px;
  line-height: 1.65;
  resize: vertical;
}

.editorInput:focus {
  outline: none;
  border-color: var(--dsw-static-blue-400);
}

.editorActions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("css ok")

# i18n
pairs_zh = [("odsEdited", "已编辑")]
pairs_en = [("odsEdited", "Edited")]
for path, pairs in (("src/i18n/zh.ts", pairs_zh), ("src/i18n/en.ts", pairs_en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    missing = [f"  {k}: '{v}',\n" for k, v in pairs if f"{k}:" not in t]
    if missing:
        t = t.replace(tail, "".join(missing) + tail, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("i18n", path)
