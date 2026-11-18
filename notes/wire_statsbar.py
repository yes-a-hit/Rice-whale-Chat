import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\chatInput\ChatInput.tsx")
t = io.open(p, encoding="utf-8").read()

# 1) 引入用量条
t = t.replace(
    "import styles from './ChatInput.module.css'",
    "import { SessionStatsBar } from '../billing/SessionStatsBar.js'\nimport styles from './ChatInput.module.css'",
    1,
)

# 2) 外层包 fragment，输入框下方挂用量条
old = """  return (
    <div
      className={clsx(styles.wrapper, sessionId === null ? styles.home : styles.session)}"""
new = """  return (
    <>
      <div
        className={clsx(styles.wrapper, sessionId === null ? styles.home : styles.session)}"""
assert old in t
t = t.replace(old, new, 1)

old = """      {dragging ? <DragMask /> : null}
    </div>
  )
}"""
new = """        {dragging ? <DragMask /> : null}
      </div>
      <SessionStatsBar sessionId={sessionId} />
    </>
  )
}"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ChatInput wired")
