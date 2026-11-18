import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

p = root / "src/components/chatInput/ChatInput.tsx"
t = io.open(p, encoding="utf-8").read()

# 从 toggles 内部挪到外面：toggles 在空间不足时会折叠成只剩图标，
# 模型名必须一直可见，所以放在 functionRow 的第一个位置。
t = t.replace(
    "        <div ref={togglesRef} className={styles.toggles}>\n          <ModelPicker />",
    "        <ModelPicker />\n        <div ref={togglesRef} className={styles.toggles}>",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("moved")

p = root / "src/components/chatInput/ChatInput.module.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """.modelGroup {
  display: flex;
  gap: 2px;
  padding: 2px;
  border-radius: 10px;
  background: var(--dsw-alias-bg-elevated);
}""",
    """.modelGroup {
  display: flex;
  flex-shrink: 0;
  gap: 2px;
  margin-right: 2px;
  padding: 2px;
  border-radius: 10px;
  background: var(--dsw-alias-bg-elevated);
}

/* 模型名一直显示，不参与 toggles 的「空间不足只留图标」折叠 */
.modelGroup .toggleLabel {
  display: inline;
}""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("css ok")
