import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 没 Key 不再自动弹设置，改由欢迎页的图 + 按钮引导 ----------
p = root / "src/components/settings/settingsDialogState.ts"
t = io.open(p, encoding="utf-8").read()
old = """/** 没有 API Key 时打开设置并选中 API Key 所在的「数据管理」，返回是否已有 Key */
export const ensureApiKey = () => {
  if (useSettings.getState().apiKey) {
    return true
  }
  openSettings('data')
  return false
}"""
new = """/**
 * 是否已有 API Key。
 * 没有 Key 时不再强行弹设置——欢迎页会用角色图 + 「去设置」按钮引导，
 * 长辈第一次打开看到的是图，不是一屏表单。
 */
export const ensureApiKey = () => Boolean(useSettings.getState().apiKey)"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ensureApiKey ok")

# ---------- 2. 欢迎图放大一点 ----------
p = root / "src/components/session/Welcome.module.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """.mascotImage {
  width: min(300px, 62vw);
  max-height: 36vh;
  object-fit: contain;
  /* 图片本身是白底，圆角一下更像贴纸 */
  border-radius: 16px;
  user-select: none;
  -webkit-user-drag: none;
}""",
    """.mascotImage {
  width: min(340px, 74vw);
  max-height: 44vh;
  object-fit: contain;
  user-select: none;
  -webkit-user-drag: none;
}""",
    1,
)
t = t.replace(
    """  .mascotImage {
    width: min(240px, 56vw);
    max-height: 30vh;
  }""",
    """  .mascotImage {
    width: min(330px, 78vw);
    max-height: 46vh;
  }""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("welcome image size ok")
