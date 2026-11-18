import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\services\chat\reply.ts")
t = io.open(p, encoding="utf-8").read()

old = """  // 辅助层只注入一次：历史里没有规则标记就插一对消息，之后随历史滚动
  if (auxBlock && !hasAuxInjected(history.map((message) => message.content ?? ''))) {
    messages.push({ role: 'user', content: auxBlock }, { role: 'assistant', content: '明白，按这套规则来。' })
  }"""
new = """  // 辅助层只注入一次：历史里没有规则标记就插一对消息，之后随历史滚动
  const userTexts = history
    .filter((message): message is UserMessage => message.role === 'user')
    .map((message) => message.content ?? '')
  if (auxBlock && !hasAuxInjected(userTexts)) {
    messages.push(
      { role: 'user', content: auxBlock },
      { role: 'assistant', content: [{ type: 'text', text: '明白，按这套规则来。' }] }
    )
  }"""
assert old in t
t = t.replace(old, new, 1)

# import promptLayers
if "from './promptLayers.js'" not in t:
    t = t.replace(
        "} from './types.js'",
        "} from './types.js'\nimport { hasAuxInjected } from './promptLayers.js'",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("reply fixed")
