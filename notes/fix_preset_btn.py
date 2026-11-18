import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 按钮文案：用「编辑」而不是「编辑消息」
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "          <button type=\"button\" className={styles.ghostButton} onClick={() => startEdit(preset.id)}>\n            {t('editMessage')}\n          </button>",
    "          <button type=\"button\" className={styles.ghostButton} onClick={() => startEdit(preset.id)}>\n            {t('odsPresetEdit')}\n          </button>",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("btn ok")

pairs_zh = [("odsPresetEdit", "编辑")]
pairs_en = [("odsPresetEdit", "Edit")]
for path, pairs in (("src/i18n/zh.ts", pairs_zh), ("src/i18n/en.ts", pairs_en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    missing = [f"  {k}: '{v}',\n" for k, v in pairs if f"{k}:" not in t]
    if missing:
        t = t.replace(tail, "".join(missing) + tail, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("i18n ok")
