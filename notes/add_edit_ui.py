import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- UI ----------
p = root / "src/components/messages/AssistantMessage.tsx"
t = io.open(p, encoding="utf-8").read()

# 1. 状态
if "const [editing" not in t:
    t = t.replace(
        "  const summaryEntry = `${message.id}-summary`",
        """  const summaryEntry = `${message.id}-summary`
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState('')
  const startEditing = () => {
    setDraft(answer?.text ?? '')
    setEditing(true)
  }
  const saveEditing = () => {
    if (editReply(sessionId, message.id, draft)) {
      setEditing(false)
    }
  }""",
        1,
    )

# 2. 正文区：编辑态用 textarea
if "styles.editor" not in t:
    t = t.replace(
        """      {answer ? (
        <Markdown
          className="ds-assistant-message-main-content"
          content={answer.markdown}
          loading={streaming}
          cacheKey={message.id}
          disableLink={false}
          sources={view.sources}
        />
      ) : null}""",
        """      {editing ? (
        <div className={styles.editor}>
          <textarea
            className={styles.editorInput}
            value={draft}
            autoFocus
            rows={Math.min(18, Math.max(4, draft.split('\\n').length + 1))}
            onChange={(event) => setDraft(event.target.value)}
          />
          <div className={styles.editorActions}>
            <Button size="md" variant="secondary" onClick={() => setEditing(false)}>
              {t('cancel')}
            </Button>
            <Button size="md" variant="primary" onClick={saveEditing}>
              {t('save')}
            </Button>
          </div>
        </div>
      ) : answer ? (
        <Markdown
          className="ds-assistant-message-main-content"
          content={answer.markdown}
          loading={streaming}
          cacheKey={message.id}
          disableLink={false}
          sources={view.sources}
        />
      ) : null}""",
        1,
    )

# 3. 操作条：加编辑、删除
if "IconEditOutline16" not in t:
    t = t.replace(
        """            <IconButton
              icon={<IconRefreshOutline16 />}
              tooltip={t('regenerate')}""",
        """            <IconButton
              icon={<IconEditOutline16 />}
              tooltip={t('edit')}
              tooltipPlacement="bottom"
              disabled={busy || !answer}
              onClick={startEditing}
            />
            <IconButton
              icon={<IconTrashOutline16 />}
              tooltip={t('delete')}
              tooltipPlacement="bottom"
              disabled={busy}
              onClick={() => deleteMessage(sessionId, message.id)}
            />
            <IconButton
              icon={<IconRefreshOutline16 />}
              tooltip={t('regenerate')}""",
        1,
    )

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ui ok")
