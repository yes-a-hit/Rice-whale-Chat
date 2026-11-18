import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. DataSection 用统一的按钮样式 ----------
p = root / "src/components/settings/DataSection.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import styles from './Settings.module.css'",
    "import ext from './Ext.module.css'",
    1,
)
t = t.replace("<div className={styles.deleteActions}>", "<div className={ext.fieldRow}>")
t = t.replace("className={styles.cellButton}", "className={ext.ghostButton}")
# 余额刷新按钮用主色
t = t.replace(
    '<button type="button" className={ext.ghostButton} disabled={loading || !apiKey} onClick={refresh}>',
    '<button type="button" className={ext.saveButton} disabled={loading || !apiKey} onClick={refresh}>',
)
# 读取失败也要能看出来
t = t.replace(
    """  const refresh = () => {
    void readLocalStats().then(setStats)
  }""",
    """  const refresh = () => {
    void readLocalStats()
      .then(setStats)
      .catch(() => setStats(null))
  }""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("DataSection styles ok")

# ---------- 2. 角色卡文案：与系统提示词独立 ----------
zh_path = root / "src/i18n/zh.ts"
t = io.open(zh_path, encoding="utf-8").read()
t = t.replace(
    "odsCardHint: '导入 PNG 或 JSON 角色卡（chara card v2），会写入系统提示词',",
    "odsCardHint: '导入 PNG 或 JSON 角色卡（chara card v2）；角色设定独立于系统提示词，两者同时生效',",
)
io.open(zh_path, "w", encoding="utf-8", newline="\n").write(t)
print("card hint ok")

# ---------- 3. Lite 模式默认打开深度思考 ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
old = """export const setUiMode = (uiMode: UiMode) => {"""
new = """export const setUiMode = (uiMode: UiMode) => {
  // Lite 面向长辈：默认打开深度思考，回答更靠谱
  if (uiMode === 'lite' && !useSettings.getState().thinking) {
    setThinking(true)
  }"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("lite thinking ok")
