import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

zh = [
    ("odsOnboardTitle", "选一个用起来舒服的模式"),
    ("odsOnboardSubtitle", "两个模式共用同一份聊天记录与密钥，随时能在设置里切换。"),
    ("odsOnboardLiteDesc", "字大、按钮少、回复自动朗读，适合爸妈和长辈日常用；也能语音说话提问。"),
    ("odsOnboardPlusDesc", "完整功能：思考过程、联网搜索、附件、分支、提示词与角色卡、皮肤与生图。"),
    ("odsOnboardHint", "先选一个就行，之后在设置「扩展」里随时改。"),
]
en = [
    ("odsOnboardTitle", "Pick the mode that feels right"),
    ("odsOnboardSubtitle", "Both modes share the same chats and key, and you can switch anytime."),
    ("odsOnboardLiteDesc", "Big text, few buttons, replies read aloud. Good for parents and daily use."),
    ("odsOnboardPlusDesc", "Everything: thinking, web search, attachments, branches, prompts, character cards, skins and images."),
    ("odsOnboardHint", "Pick one now; change it later in Settings → Extensions."),
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
