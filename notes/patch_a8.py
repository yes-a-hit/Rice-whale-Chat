import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- store.ts: 回复完成时广播事件 ----------
p = root / "src/services/chat/store.ts"
t = io.open(p, encoding="utf-8").read()
anchor = "import { createLatestReminder } from './latestReminder.js'"
assert anchor in t
t = t.replace(anchor, anchor + "\nimport { emitReplyDone } from './replyEvents.js'", 1)

old = """    persist(sessionId)
  }
}"""
new = """    persist(sessionId)
    if (reply.status === 'done') {
      emitReplyDone(sessionId, reply.id)
    }
  }
}"""
assert t.count(old) == 1
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched store.ts")

# ---------- App.tsx: Lite 模式自动朗读 ----------
p = root / "src/app/App.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { stopReadAloud } from '../services/speech/readAloud.js'",
    "import { describeReadAloudError, stopReadAloud, toggleReadAloud } from '../services/speech/readAloud.js'\n"
    "import { onReplyDone } from '../services/chat/replyEvents.js'\n"
    "import { getReplyText } from '../services/chat/reply.js'",
    1,
)
hook_anchor = "  // 切换会话时停止朗读\n  useEffect(stopReadAloud, [activeId])"
assert hook_anchor in t
t = t.replace(
    hook_anchor,
    hook_anchor
    + """

  // Lite 模式：回复完成后自动朗读，长辈不用去找小喇叭按钮
  useEffect(
    () =>
      onReplyDone((sessionId, messageId) => {
        if (useSettings.getState().uiMode !== 'lite') {
          return
        }
        const state = useChatStore.getState()
        if (state.activeId !== sessionId) {
          return
        }
        const message = state.sessionCache[sessionId]?.messages.find((item) => item.id === messageId)
        if (!message || message.role !== 'assistant') {
          return
        }
        const text = getReplyText(message)
        if (text.trim()) {
          toggleReadAloud(messageId, text, (error) => showToast(describeReadAloudError(error)))
        }
      }),
    []
  )""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("patched App.tsx")
