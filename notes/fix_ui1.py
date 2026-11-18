import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 设置弹窗移动端布局 ----------
p = root / "src/components/settings/Settings.module.css"
t = io.open(p, encoding="utf-8").read()
old = """  .dialog {
    align-self: flex-end;
    width: 100%;
    max-width: none;
    height: calc(100% - 64px);
    max-height: 800px;
    border-radius: 24px 24px 0 0;
  }"""
new = """  .dialog {
    align-self: flex-end;
    box-sizing: border-box;
    width: 100%;
    max-width: 100%;
    height: calc(100% - 56px);
    max-height: none;
    margin: 0;
    padding: 16px 16px calc(12px + env(safe-area-inset-bottom));
    border-radius: 20px 20px 0 0;
    overflow: hidden;
  }"""
assert old in t
t = t.replace(old, new, 1)

old2 = """  .content {
    padding-top: 24px;
    padding-left: 0;
    padding-bottom: env(safe-area-inset-bottom);
  }"""
new2 = """  .content {
    padding-top: 16px;
    padding-left: 0;
    padding-right: 4px;
    padding-bottom: calc(8px + env(safe-area-inset-bottom));
    overflow-y: auto;
    overscroll-behavior: contain;
    -webkit-overflow-scrolling: touch;
  }

  .navigation {
    scrollbar-width: none;
  }

  .navigation::-webkit-scrollbar {
    display: none;
  }"""
assert old2 in t
t = t.replace(old2, new2, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settings css ok")

# ---------- 2. index.html viewport ----------
p = root / "src/index.html"
t = io.open(p, encoding="utf-8").read()
old = '<meta name="viewport" content="width=device-width,initial-scale=1" />'
new = (
    '<meta name="viewport" content="width=device-width,initial-scale=1,'
    'viewport-fit=cover" />'
)
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("index.html ok")

# ---------- 3. App.module.css 安全区 ----------
p = root / "src/app/App.module.css"
t = io.open(p, encoding="utf-8").read()
old = """@media not all and (min-width: 768px) {
  .frame {
    position: fixed;
    top: var(--app-viewport-top, 0px);
    bottom: auto;
    height: var(--app-viewport-height, 100dvh);
  }
}"""
new = """@media not all and (min-width: 768px) {
  .frame {
    position: fixed;
    top: var(--app-viewport-top, 0px);
    left: 0;
    right: 0;
    bottom: auto;
    width: auto;
    height: var(--app-viewport-height, 100dvh);
    /* 刘海屏与手势条：内容不贴边 */
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
    box-sizing: border-box;
  }
}"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("app css ok")
