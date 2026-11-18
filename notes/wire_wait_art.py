import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 余额不足时给一张「等会再来」的鲸鱼娘 ----------
p = root / "src/components/messages/AssistantMessage.tsx"
t = io.open(p, encoding="utf-8").read()
old = """      ) : notice ? (
        <div className={styles.notice}>
          <IconWarningOutline16 />"""
new = """      ) : notice ? (
        <div className={styles.notice}>
          {notice.action === 'topUp' ? (
            <img className={styles.noticeArt} src="/media/wait.png" alt="" aria-hidden />
          ) : (
            <IconWarningOutline16 />
          )}"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("notice art ok")

# 样式
p = root / "src/components/messages/AssistantMessage.module.css"
t = io.open(p, encoding="utf-8").read()
if ".noticeArt" not in t:
    t = t.rstrip("\n") + """

.noticeArt {
  width: 96px;
  height: auto;
  flex-shrink: 0;
  margin-bottom: 4px;
  user-select: none;
  -webkit-user-drag: none;
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("css ok")
