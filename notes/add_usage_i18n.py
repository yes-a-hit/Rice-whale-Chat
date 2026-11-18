import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

zh = [
    ("odsStatsTurns", "{count} 轮"),
    ("odsStatsSteps", "{count} 段"),
    ("odsStatsSpeed", "{value} tok/s"),
    ("odsStatsTokens", "{value} tok"),
    ("odsStatsCache", "缓存 {value}%"),
    ("odsStatsContext", "上下文 {value}%"),
    ("odsStatsContextHint", "最近一轮占用的上下文窗口（128K）"),
    ("odsUsageSection", "用量"),
    ("odsUsageTitle", "用量与计费"),
    ("odsUsageSubtitle", "按 DeepSeek 官方价估算，仅供参考"),
    ("odsUsageCacheHit", "缓存命中"),
    ("odsUsageInput", "输入（未命中）"),
    ("odsUsageOutput", "输出"),
    ("odsUsageSearch", "联网检索"),
    ("odsUsageTotal", "合计"),
    ("odsUsageTokensUnit", "tok"),
    ("odsUsageTimesUnit", "次"),
    ("odsUsageEmpty", "这个会话还没有用量数据"),
    ("odsUsagePriceHint", "命中 ¥0.2 / 未命中 ¥2 / 输出 ¥3（每百万 token），检索 ¥0.01 每次"),
    ("odsUsageSpeed", "生成速率"),
    ("odsUsageElapsed", "累计耗时"),
    ("odsUsageContext", "上下文占用"),
    ("odsUsageSession", "当前会话"),
]
en = [
    ("odsStatsTurns", "{count} turns"),
    ("odsStatsSteps", "{count} parts"),
    ("odsStatsSpeed", "{value} tok/s"),
    ("odsStatsTokens", "{value} tok"),
    ("odsStatsCache", "{value}% cached"),
    ("odsStatsContext", "{value}% ctx"),
    ("odsStatsContextHint", "Context window used by the latest turn (128K)"),
    ("odsUsageSection", "Usage"),
    ("odsUsageTitle", "Usage and cost"),
    ("odsUsageSubtitle", "Estimated with DeepSeek list prices"),
    ("odsUsageCacheHit", "Cache hit"),
    ("odsUsageInput", "Input (miss)"),
    ("odsUsageOutput", "Output"),
    ("odsUsageSearch", "Web search"),
    ("odsUsageTotal", "Total"),
    ("odsUsageTokensUnit", "tok"),
    ("odsUsageTimesUnit", "req"),
    ("odsUsageEmpty", "No usage recorded for this chat yet"),
    ("odsUsagePriceHint", "hit 0.2 / miss 2 / output 3 per 1M tokens, search 0.01 each"),
    ("odsUsageSpeed", "Generation rate"),
    ("odsUsageElapsed", "Total time"),
    ("odsUsageContext", "Context used"),
    ("odsUsageSession", "Current chat"),
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
