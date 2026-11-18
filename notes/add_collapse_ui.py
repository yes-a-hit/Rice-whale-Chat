import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\settings\ExtSettings.tsx")
t = io.open(p, encoding="utf-8").read()

if "odsCollapseThinking" not in t:
    # 在 DefaultToggleSettings 的返回里追加一格
    anchor = """      <SettingCell
        label={t('odsDefaultThinking')}"""
    addition = """      <SettingCell
        label={t('odsCollapseThinking')}
        description={t('odsCollapseThinkingHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={collapseThinking}
            className={clsx(styles.switch, collapseThinking && styles.switchOn)}
            onClick={() => setCollapseThinking(!collapseThinking)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />
"""
    assert anchor in t
    t = t.replace(anchor, addition + anchor, 1)
    t = t.replace(
        """  const search = useSettings((state) => state.search)
  return (
    <>""",
        """  const search = useSettings((state) => state.search)
  const collapseThinking = useSettings((state) => state.collapseThinking)
  return (
    <>""",
        1,
    )
    # setter 导入
    if "setCollapseThinking" not in t.split("const DefaultToggleSettings")[0]:
        t = t.replace(
            "import { setSearch, setThinking,",
            "import { setCollapseThinking, setSearch, setThinking,",
            1,
        )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("toggle cell ok")
else:
    print("already")
