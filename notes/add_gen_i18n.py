import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

zh = [
    ("odsGenerationTitle", "生成参数"),
    ("odsSafetyCheck", "发送 safety_check: high"),
    ("odsSafetyCheckHint", "关掉后请求里不带该字段，服务端按最低档处理；Plus 建议关"),
    ("odsTemperature", "温度 temperature"),
    ("odsTemperatureHint", "0–2，留空用服务端默认；思考模式下服务端会锁定为 1"),
    ("odsTopP", "Top P"),
    ("odsTopPHint", "0.01–1，留空用服务端默认"),
    ("odsMaxTokens", "最大输出 max_tokens"),
    ("odsMaxTokensHint", "留空不发送；太小会把思考一起截断"),
    ("odsParamUnset", "默认"),
]
en = [
    ("odsGenerationTitle", "Generation"),
    ("odsSafetyCheck", "Send safety_check: high"),
    ("odsSafetyCheckHint", "Off removes the field, the server falls back to its lowest level"),
    ("odsTemperature", "Temperature"),
    ("odsTemperatureHint", "0-2, empty uses server default; thinking mode pins it to 1"),
    ("odsTopP", "Top P"),
    ("odsTopPHint", "0.01-1, empty uses server default"),
    ("odsMaxTokens", "Max output tokens"),
    ("odsMaxTokensHint", "Empty means not sent; too low truncates thinking"),
    ("odsParamUnset", "default"),
]

for path, pairs in (("src/i18n/zh.ts", zh), ("src/i18n/en.ts", en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    if pairs[0][0] in t:
        print("skip", path)
        continue
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    block = "".join(f"  {k}: '{v}',\n" for k, v in pairs)
    t = t.replace(tail, block + tail, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("ok", path)

# 把 <GenerationSettings /> 挂上去
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()
if "<GenerationSettings />" not in t:
    lines = t.split("\n")
    for i, line in enumerate(lines):
        if "<DefaultToggleSettings />" in line:
            indent = line[: len(line) - len(line.lstrip())]
            lines.insert(i + 1, f"{indent}<GenerationSettings />")
            print("inserted at line", i + 2)
            break
    t = "\n".join(lines)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
