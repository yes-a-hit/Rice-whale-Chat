import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

p = root / "src/services/chat/types.ts"
t = io.open(p, encoding="utf-8").read()

# Session 加 archived
t = t.replace(
    """export type Session = {
  id: string
  title: string
  createdAt: number
  updatedAt: number""",
    """export type Session = {
  id: string
  title: string
  createdAt: number
  updatedAt: number
  /** 已归档：默认不在侧栏主列表显示 */
  archived?: boolean""",
    1,
)
# Summary 带上 archived
t = t.replace(
    "export type SessionSummary = Pick<Session, 'id' | 'title' | 'createdAt' | 'updatedAt'>",
    "export type SessionSummary = Pick<\n  Session,\n  'id' | 'title' | 'createdAt' | 'updatedAt' | 'archived'\n>",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("types ok")

# toSessionSummary 要带上 archived
p = root / "src/services/chat/types.ts"
t = io.open(p, encoding="utf-8").read()
if "toSessionSummary" in t:
    print("has toSessionSummary in types")
p = root / "src/services/chat/db.ts"
t = io.open(p, encoding="utf-8").read()
if "toSessionSummary" in t:
    print("defined in db.ts")
