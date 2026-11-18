import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- speech.ts ----------
p = root / "src/services/api/speech.ts"
text = io.open(p, encoding="utf-8").read()
text = text.replace(
    "import { ApiError, API_ORIGIN, request } from './client.js'",
    "import { ApiError, getApiOrigin, request } from './client.js'",
)
old = "const TOOLS_BASE_URL = `${API_ORIGIN}/v1/tools`"
assert old in text
text = text.replace(old, "const toolsBaseUrl = () => `${getApiOrigin()}/v1/tools`")
text = text.replace("${TOOLS_BASE_URL}", "${toolsBaseUrl()}")
io.open(p, "w", encoding="utf-8", newline="\n").write(text)
print("patched speech.ts")

# ---------- index.html ----------
p = root / "src/index.html"
text = io.open(p, encoding="utf-8").read()
text = text.replace("<title>API 使用 demo</title>", "<title>Open DeepSeek</title>")
io.open(p, "w", encoding="utf-8", newline="\n").write(text)
print("patched index.html")

# ---------- package.json ----------
p = root / "package.json"
text = io.open(p, encoding="utf-8").read()
text = text.replace('"name": "chat-demo"', '"name": "open-deepseek-chat"')
text = text.replace(
    '"description": "基于 DeepSeek API 的静态聊天示例。"',
    '"description": "Open DeepSeek：基于 chat-demo 的双模式本地增强聊天前端（Lite / Plus）。"',
)
io.open(p, "w", encoding="utf-8", newline="\n").write(text)
print("patched package.json")
