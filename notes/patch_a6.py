import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

zh = [
    ("odsLocalTtsMissing", "本地语音模型还没下载，请到「扩展 → 模型」里下载后再试"),
    ("odsSystemTtsUnavailable", "这台设备没有可用的系统语音引擎"),
]
en = [
    ("odsLocalTtsMissing", "The local voice model is not downloaded yet"),
    ("odsSystemTtsUnavailable", "No system speech engine is available on this device"),
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
