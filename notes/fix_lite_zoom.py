import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. skins.ts：把 zoom 暴露成 CSS 变量 ----------
p = root / "src/app/skins.ts"
t = io.open(p, encoding="utf-8").read()
old = """  // 手机端用 zoom 放大整体界面，比逐个改字号可靠
  root.style.zoom = fontScale === 1 ? '' : String(fontScale)"""
new = """  // 手机端用 zoom 放大整体界面，比逐个改字号可靠。
  // 同时把倍率写进 --ods-zoom，让 fixed 布局按倍率反算高度，
  // 否则 100dvh 被放大后底部输入框会被裁掉（老登模式「UI 过大遮挡信息」的根因）。
  root.style.setProperty('--ods-zoom', String(fontScale))
  root.style.zoom = fontScale === 1 ? '' : String(fontScale)"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("skins.ts ok")

# ---------- 2. frame 高度按 zoom 反算 ----------
p = root / "src/app/App.module.css"
t = io.open(p, encoding="utf-8").read()
old = """  .frame {
    position: fixed;
    top: var(--app-viewport-top, 0px);
    left: 0;
    right: 0;
    bottom: auto;
    width: auto;
    height: var(--app-viewport-height, 100dvh);"""
new = """  .frame {
    position: fixed;
    /* zoom 会把 px 等比放大，视口高度是物理像素，这里要除回倍率 */
    top: calc(var(--app-viewport-top, 0px) / var(--ods-zoom, 1));
    left: 0;
    right: 0;
    bottom: auto;
    width: auto;
    height: calc(var(--app-viewport-height, 100dvh) / var(--ods-zoom, 1));"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("App.module.css ok")

# ---------- 3. Lite 默认倍率降到 1.08 ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "write(KEYS.fontScale, uiMode === 'lite' ? '1.15' : '1')",
    "write(KEYS.fontScale, uiMode === 'lite' ? '1.08' : '1')",
)
t = t.replace(
    "useSettings.setState({ uiMode, fontScale: uiMode === 'lite' ? 1.15 : 1 })",
    "useSettings.setState({ uiMode, fontScale: uiMode === 'lite' ? 1.08 : 1 })",
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settings.ts ok")
