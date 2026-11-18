import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 修正 ExtSettings 里引用的音色 key
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("label: t('ttsVoiceStella')", "label: t('settingsTtsVoiceStella')")
t = t.replace("label: t('ttsVoiceTide')", "label: t('settingsTtsVoiceTide')")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("voice keys fixed")

zh = [
    ("odsTtsRate", "朗读语速"),
    ("odsTtsRateHint", "当前 {rate} 倍速；长辈建议 0.9～1.1"),
    ("odsTtsSystemVoice", "系统语音音色"),
    ("odsTtsSystemVoiceHint", "只列出手机里已安装的中文语音"),
    ("odsTtsSystemVoiceAuto", "自动（优先离线中文语音）"),
    ("odsTtsCloudVoice", "云端音色"),
    ("odsTtsCloudVoiceHint", "走官方接口时可用"),
]
en = [
    ("odsTtsRate", "Speaking rate"),
    ("odsTtsRateHint", "Currently {rate}x; 0.9-1.1 suits most listeners"),
    ("odsTtsSystemVoice", "System voice"),
    ("odsTtsSystemVoiceHint", "Only Chinese voices installed on the device are listed"),
    ("odsTtsSystemVoiceAuto", "Auto (prefer offline Chinese voice)"),
    ("odsTtsCloudVoice", "Cloud voice"),
    ("odsTtsCloudVoiceHint", "Used when reading through the official API"),
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
