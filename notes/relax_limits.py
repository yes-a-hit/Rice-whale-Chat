import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. parseEvent：不再丢弃非白名单 stop_reason ----------
p = root / "src/services/api/parseEvent.ts"
t = io.open(p, encoding="utf-8").read()
old = """    case 'message_delta':
      if (
        !isRecord(value.delta) ||
        !['end_turn', 'max_tokens', 'tool_use', 'refusal'].includes(
          value.delta.stop_reason as string
        )
      ) {
        return null
      }"""
new = """    case 'message_delta':
      // 原版只认 end_turn/max_tokens/tool_use/refusal 四种 stop_reason，
      // 遇到新值会把整条 message_delta 丢掉，连 usage 一起丢；这里照收。
      if (!isRecord(value.delta)) {
        return null
      }"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("parseEvent ok")

# ---------- 2. Lite 首次默认打开深度思考 ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
old = "  thinking: read(KEYS.thinking) === 'true',"
new = """  // Lite 没手动设过时默认打开深度思考（长辈问复杂问题更靠谱）
  thinking:
    read(KEYS.thinking) === 'true' ||
    (read(KEYS.thinking) === null && initialUiMode() === 'lite'),"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("thinking default ok")
