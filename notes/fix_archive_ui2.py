import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

p = root / "src/services/chat/types.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """export const toSessionSummary = (session: SessionSummary): SessionSummary => ({
  id: session.id,
  title: session.title,
  createdAt: session.createdAt,
  updatedAt: session.updatedAt,
})""",
    """export const toSessionSummary = (session: SessionSummary): SessionSummary => ({
  id: session.id,
  title: session.title,
  createdAt: session.createdAt,
  updatedAt: session.updatedAt,
  ...(session.archived ? { archived: true } : {}),
})""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("summary ok")

# 菜单去掉不存在的图标
p = root / "src/components/sider/SessionItem.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("import { IconArchiveOutline16 } from '../base/icons.js'\n", "", 1)
t = t.replace("              icon: <IconArchiveOutline16 />,\n", "", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("icon removed")

# i18n
pairs_zh = [
    ("odsArchive", "归档"),
    ("odsUnarchive", "取消归档"),
    ("odsArchivedChats", "已归档"),
    ("odsBackToChats", "返回对话"),
]
pairs_en = [
    ("odsArchive", "Archive"),
    ("odsUnarchive", "Unarchive"),
    ("odsArchivedChats", "Archived"),
    ("odsBackToChats", "Back to chats"),
]
for path, pairs in (("src/i18n/zh.ts", pairs_zh), ("src/i18n/en.ts", pairs_en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    missing = [f"  {k}: '{v}',\n" for k, v in pairs if f"{k}:" not in t]
    if missing:
        t = t.replace(tail, "".join(missing) + tail, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("i18n ok")
