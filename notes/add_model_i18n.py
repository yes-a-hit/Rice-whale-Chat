import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. i18n ----------
pairs_zh = [
    ("odsModelFlash", "快速"),
    ("odsModelPro", "专家"),
    ("odsModel", "模型"),
    ("odsCollapseThinking", "自动折叠思考内容"),
    ("odsCollapseThinkingHint", "开启后思考完就收起来，只留一行标题，点一下再展开"),
]
pairs_en = [
    ("odsModelFlash", "Fast"),
    ("odsModelPro", "Pro"),
    ("odsModel", "Model"),
    ("odsCollapseThinking", "Auto-collapse thinking"),
    ("odsCollapseThinkingHint", "Fold the thinking block once it finishes; tap the title to expand"),
]
for path, pairs in (("src/i18n/zh.ts", pairs_zh), ("src/i18n/en.ts", pairs_en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    missing = [f"  {k}: '{v}',\n" for k, v in pairs if f"{k}:" not in t]
    if missing:
        t = t.replace(tail, "".join(missing) + tail, 1)
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("i18n ok", path)
