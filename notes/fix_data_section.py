import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 设置的数据管理页接入 DataSection ----------
p = root / "src/components/settings/SettingsDialog.tsx"
t = io.open(p, encoding="utf-8").read()
if "DataSection" not in t:
    t = t.replace(
        "import { SettingCell } from './SettingCell.js'",
        "import { SettingCell } from './SettingCell.js'\nimport { DataSection } from './DataSection.js'",
        1,
    )
    old = """            <>
              <ApiKeyField editor={apiKeyEditor} />"""
    new = """            <>
              <DataSection />
              <ApiKeyField editor={apiKeyEditor} />"""
    assert old in t
    t = t.replace(old, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("SettingsDialog ok")

zh = [
    ("odsBalance", "账户余额"),
    ("odsBalanceHint", "点刷新查询"),
    ("odsBalanceLoading", "查询中…"),
    ("odsBalanceRefresh", "刷新"),
    ("odsBalanceNoKey", "还没填 API Key"),
    ("odsBalanceUnavailable", "余额不足"),
    ("odsBalanceFailed", "查询失败：{message}"),
    ("odsLocalDb", "本地数据库"),
    ("odsLocalDbLoading", "读取中…"),
    ("odsLocalDbStats", "{sessions} 个会话 · {messages} 条消息 · 占用 {usage} / 可用 {quota}"),
    ("odsLocalDbRefresh", "刷新"),
    ("odsClearCache", "清理缓存"),
    ("odsCacheCleared", "缓存已清理"),
]
en = [
    ("odsBalance", "Balance"),
    ("odsBalanceHint", "Tap refresh to query"),
    ("odsBalanceLoading", "Checking..."),
    ("odsBalanceRefresh", "Refresh"),
    ("odsBalanceNoKey", "No API key yet"),
    ("odsBalanceUnavailable", "Insufficient balance"),
    ("odsBalanceFailed", "Failed: {message}"),
    ("odsLocalDb", "Local database"),
    ("odsLocalDbLoading", "Reading..."),
    ("odsLocalDbStats", "{sessions} chats - {messages} messages - {usage} of {quota} used"),
    ("odsLocalDbRefresh", "Refresh"),
    ("odsClearCache", "Clear cache"),
    ("odsCacheCleared", "Cache cleared"),
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
