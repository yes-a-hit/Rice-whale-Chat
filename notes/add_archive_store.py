import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 类型：会话加 archived ----------
p = root / "src/services/chat/types.ts"
t = io.open(p, encoding="utf-8").read()
if "archived?" not in t:
    t = t.replace(
        "export type SessionSummary = {",
        "export type SessionSummary = {\n  /** 归档：不在主列表里显示，需要切到「已归档」才看得到 */\n  archived?: boolean",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("summary type ok")

# Session 主体也加（如果存在独立定义）
if "export type Session = " in t and "archived?" in t:
    pass
print("types done")

# ---------- 2. store：archiveSession ----------
p = root / "src/services/chat/store.ts"
t = io.open(p, encoding="utf-8").read()
if "export const archiveSession" not in t:
    block = '''
/** 归档 / 取消归档一个会话 */
export const archiveSession = (id: string, archived: boolean) => {
  const session = getSession(id)
  if (session) {
    updateSession(id, (value) => ({ ...value, archived }))
  }
  useChatStore.setState((state) => ({
    sessions: state.sessions.map((item) => (item.id === id ? { ...item, archived } : item)),
  }))
  persist(id)
}
'''
    anchor = "export const removeSession = "
    assert anchor in t
    t = t.replace(anchor, block.lstrip("\n") + "\n" + anchor, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("store ok")
