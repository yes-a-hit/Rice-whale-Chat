import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- ChatInput: Lite 模式隐藏思考/搜索开关 ----------
p = root / "src/components/chatInput/ChatInput.tsx"
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    "  const thinking = useSettings((state) => state.thinking)",
    "  const uiMode = useSettings((state) => state.uiMode)\n"
    "  const thinking = useSettings((state) => state.thinking)",
    1,
)
t = t.replace(
    '        <div ref={togglesRef} className={styles.toggles}>',
    '        <div\n'
    '          ref={togglesRef}\n'
    '          className={clsx(styles.toggles, uiMode === \'lite\' && styles.togglesHidden)}\n'
    '        >',
    1,
)
t = t.replace(
    "          {useSettings((state) => state.uiMode) === 'plus' ? (",
    "          {uiMode === 'plus' ? (",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ChatInput ok")

# ---------- CSS ----------
p = root / "src/components/chatInput/ChatInput.module.css"
t = io.open(p, encoding="utf-8").read()
if ".togglesHidden" not in t:
    t += """
/* Lite 模式：隐藏深度思考 / 联网搜索开关，保持界面干净 */
.togglesHidden {
  display: none;
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("css ok")
