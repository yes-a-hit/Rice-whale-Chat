import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\chatInput\ChatInput.tsx")
t = io.open(p, encoding="utf-8").read()

old = """    const raw = getDraft(sessionId)?.text?.trim() ?? ''
    const command = /^\\/(img|draw|pic)\\s+([\\s\\S]+)$/i.exec(raw)
    if (command && uiMode === 'plus') {
      openImageDialog(command[2].trim())
      setDraft(sessionId, { text: '' })
      void clearDraftText(sessionId)
      return
    }"""
new = """    const raw = getDraft(sessionId).text.trim()
    const command = /^\\/(img|draw|pic)\\s+([\\s\\S]+)$/i.exec(raw)
    if (command && uiMode === 'plus') {
      openImageDialog(command[2].trim())
      setDraftText(sessionId, '')
      return
    }"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("command fixed")
