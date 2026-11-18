import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 1. 侧栏归档按钮用图标
p = root / "src/components/sider/Sider.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "          <span className={styles.settingsIcon}>{showArchived ? 'π' : 'ϟ'}</span>",
    "          <span className={styles.settingsIcon}>\n            <IconFolderOutline16 />\n          </span>",
    1,
)
if "IconFolderOutline16" not in t.split("export const")[0]:
    t = t.replace(
        "import { IconPanelLeftOutline16 } from '../base/icons.js'",
        "import { IconFolderOutline16, IconPanelLeftOutline16 } from '../base/icons.js'",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("sider icon ok")

# 2. 已编辑标记
p = root / "src/components/messages/AssistantMessage.tsx"
t = io.open(p, encoding="utf-8").read()
if "odsEdited" not in t:
    t = t.replace(
        "          <BranchSwitcher versions={versions} disabled={busy} onSelect={onSelectVersion} />",
        "          <div className={styles.bottomMeta}>\n"
        "            <BranchSwitcher versions={versions} disabled={busy} onSelect={onSelectVersion} />\n"
        "            {message.edited ? <span className={styles.editedTag}>{t('odsEdited')}</span> : null}\n"
        "          </div>",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("edited tag ok")

# 3. 样式
p = root / "src/components/messages/AssistantMessage.module.css"
t = io.open(p, encoding="utf-8").read()
if ".editedTag" not in t:
    t += """
.bottomMeta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.editedTag {
  padding: 1px 6px;
  border-radius: 6px;
  background: var(--dsw-alias-bg-elevated);
  color: var(--dsw-alias-label-tertiary);
  font-size: 11.5px;
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("css ok")
