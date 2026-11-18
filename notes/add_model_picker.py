import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- ChatInput：插入模型选择 ----------
p = root / "src/components/chatInput/ChatInput.tsx"
t = io.open(p, encoding="utf-8").read()

if "ModelPicker" not in t:
    t = t.replace(
        "const thinking = useSettings((state) => state.thinking)",
        """/** 模型选择：Lite 用「快速 / 专家」两个胶囊，Plus 用下拉 */
const ModelPicker = () => {
  const t = useTranslate()
  const uiMode = useSettings((state) => state.uiMode)
  const model = useSettings((state) => state.model)
  if (uiMode === 'lite') {
    return (
      <div className={styles.modelGroup}>
        {CHAT_MODELS.map((item) => (
          <button
            key={item.id}
            type="button"
            className={clsx(styles.toggle, model === item.id && styles.selected)}
            aria-pressed={model === item.id}
            onClick={() => setModel(item.id)}
          >
            <span className={styles.toggleLabel}>{t(item.labelKey)}</span>
          </button>
        ))}
      </div>
    )
  }
  return (
    <select
      className={styles.modelSelect}
      aria-label={t('odsModel')}
      value={model}
      onChange={(event) => setModel(event.target.value as ChatModel)}
    >
      {CHAT_MODELS.map((item) => (
        <option key={item.id} value={item.id}>
          {t(item.labelKey)}
        </option>
      ))}
    </select>
  )
}

const thinking = useSettings((state) => state.thinking)""",
        1,
    )
    t = t.replace(
        "        <div ref={togglesRef} className={styles.toggles}>",
        "        <div ref={togglesRef} className={styles.toggles}>\n          <ModelPicker />",
        1,
    )
    t = t.replace(
        "import { setSearch, setThinking, useSettings } from '../../services/settings.js'",
        "import { setModel, setSearch, setThinking, useSettings } from '../../services/settings.js'\n"
        "import { CHAT_MODELS, type ChatModel } from '../../services/api/types.js'",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("chatinput ok")

# ---------- 样式 ----------
p = root / "src/components/chatInput/ChatInput.module.css"
t = io.open(p, encoding="utf-8").read()
if ".modelGroup" not in t:
    t += """
.modelGroup {
  display: flex;
  gap: 2px;
  padding: 2px;
  border-radius: 10px;
  background: var(--dsw-alias-bg-elevated);
}

.modelSelect {
  height: 30px;
  padding: 0 24px 0 10px;
  border: 1px solid var(--dsw-alias-border-l1);
  border-radius: 10px;
  background: var(--dsw-alias-bg-elevated);
  color: var(--dsw-alias-label-primary);
  font: inherit;
  font-size: 13px;
  appearance: none;
  cursor: pointer;
}
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("css ok")
