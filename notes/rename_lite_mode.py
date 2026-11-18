import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

zh_path = root / "src/i18n/zh.ts"
t = io.open(zh_path, encoding="utf-8").read()
t = t.replace("odsModeLite: 'Lite 老登模式',", "odsModeLite: '极简模式',")
t = t.replace(
    "odsModeHint: 'Lite 放大字号、默认朗读；Plus 开放提示词、角色卡、皮肤与生图',",
    "odsModeHint: '极简模式放大字号、默认朗读；Plus 开放提示词、角色卡、皮肤与生图',",
)
t = t.replace(
    "odsOnboardLiteDesc: '字大、按钮少、回复自动朗读，适合爸妈和长辈日常用；也能语音说话提问。',",
    "odsOnboardLiteDesc: '字大、按钮少、回复自动朗读，保留深度思考；默认不开联网搜索，适合爸妈和长辈日常用。',",
)
io.open(zh_path, "w", encoding="utf-8", newline="\n").write(t)
print("zh ok")

en_path = root / "src/i18n/en.ts"
t = io.open(en_path, encoding="utf-8").read()
t = t.replace("odsModeLite: 'Lite (simple)',", "odsModeLite: 'Minimal',")
t = t.replace(
    "odsOnboardLiteDesc: 'Big text, few buttons, replies read aloud. Good for parents and daily use.',",
    "odsOnboardLiteDesc: 'Big text, few buttons, replies read aloud, deep thinking kept on, web search off by default.',",
)
io.open(en_path, "w", encoding="utf-8", newline="\n").write(t)
print("en ok")
