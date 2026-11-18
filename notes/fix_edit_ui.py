import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# Button 的 size/variant 用本项目既有的取值；i18n 用已有 key
p = root / "src/components/messages/AssistantMessage.tsx"
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    """            <Button size="md" variant="secondary" onClick={() => setEditing(false)}>
              {t('cancel')}
            </Button>
            <Button size="md" variant="primary" onClick={saveEditing}>
              {t('save')}
            </Button>""",
    """            <Button size="s" variant="outlined" onClick={() => setEditing(false)}>
              {t('cancel')}
            </Button>
            <Button size="s" variant="primary" onClick={saveEditing}>
              {t('confirm')}
            </Button>""",
    1,
)
t = t.replace("tooltip={t('edit')}", "tooltip={t('editMessage')}", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ui fixed")

# 补 save 相关文案（有些语言包可能没有 save）
pairs_zh = [("odsSaveEdit", "保存修改")]
pairs_en = [("odsSaveEdit", "Save changes")]
for path, pairs in (("src/i18n/zh.ts", pairs_zh), ("src/i18n/en.ts", pairs_en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    missing = [f"  {k}: '{v}',\n" for k, v in pairs if f"{k}:" not in t]
    if missing:
        t = t.replace(tail, "".join(missing) + tail, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("i18n ok")
