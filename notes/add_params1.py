import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 请求类型：safety_check 可选，参数可直调 ----------
p = root / "src/services/api/types.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "  safety_check: { level: 'high' }",
    "  /** 省略即等价于 level: 'low'，Plus 模式默认不发送 */\n"
    "  safety_check?: { level: 'high' }\n"
    "  temperature?: number\n"
    "  top_p?: number\n"
    "  max_tokens?: number",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("types ok")

# ---------- 2. 设置项 ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()

if "sendSafetyCheck" not in t:
    # 类型
    t = t.replace(
        "  modelSource: ModelSource",
        "  modelSource: ModelSource\n"
        "  /** 是否在请求里带 safety_check.high；关掉等于让服务端用最低档 */\n"
        "  sendSafetyCheck: boolean\n"
        "  /** 采样参数：null 表示不发送，用服务端默认 */\n"
        "  temperature: number | null\n"
        "  topP: number | null\n"
        "  maxOutputTokens: number | null",
        1,
    )
    # 默认值
    t = t.replace(
        "  modelSource: initialModelSource(),",
        "  modelSource: initialModelSource(),\n"
        "  sendSafetyCheck: read(KEYS.sendSafetyCheck) === 'true',\n"
        "  temperature: initialNumber(KEYS.temperature),\n"
        "  topP: initialNumber(KEYS.topP),\n"
        "  maxOutputTokens: initialNumber(KEYS.maxOutputTokens),",
        1,
    )
    # KEYS
    t = t.replace(
        "  modelSource: 'ods:model-source',",
        "  modelSource: 'ods:model-source',\n"
        "  sendSafetyCheck: 'ods:send-safety-check',\n"
        "  temperature: 'ods:temperature',\n"
        "  topP: 'ods:top-p',\n"
        "  maxOutputTokens: 'ods:max-output-tokens',",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settings fields ok")
