import io, pathlib

from PIL import Image

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 界面用的小 logo ----------
out = root / "figure/out"
logo = Image.open(root / "figure/logo.png").convert("RGB")
logo.resize((128, 128), Image.LANCZOS).save(out / "logo-128.webp", "WEBP", quality=88)
print("logo-128.webp ok")

# ---------- 2. 构建时把 figure/out 拷到 dist/media ----------
p = root / "rspack.config.ts"
t = io.open(p, encoding="utf-8").read()
old = """      patterns: [{ from: path.resolve(root, 'LICENSE'), to: 'LICENSE', toType: 'file' }],"""
new = """      patterns: [
        { from: path.resolve(root, 'LICENSE'), to: 'LICENSE', toType: 'file' },
        { from: path.resolve(root, 'figure/out'), to: 'media' },
      ],"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("rspack copy ok")

# ---------- 3. Welcome 页：有 Key 用欢迎图，没 Key 用苦等图 ----------
p = root / "src/components/session/Welcome.tsx"
t = io.open(p, encoding="utf-8").read()
t = """import { useIsMobile } from '../../app/viewport.js'
import { useTranslate } from '../../i18n/index.js'
import { useSettings } from '../../services/settings.js'
import { openSettings } from '../settings/settingsDialogState.js'
import { ChatInput } from '../chatInput/ChatInput.js'
import { MobileHeader } from './MobileHeader.js'
import styles from './Welcome.module.css'

/** 新对话：角色图 + 输入框。桌面端居中；移动端输入框吸底 */
export const Welcome = () => {
  const t = useTranslate()
  const isMobile = useIsMobile()
  const hasApiKey = useSettings((state) => Boolean(state.apiKey))
  return (
    <div className={styles.container}>
      {isMobile ? <MobileHeader /> : null}
      <div className={styles.welcome}>
        <div className={styles.mascot}>
          <img
            className={styles.mascotImage}
            src={hasApiKey ? '/media/welcome.webp' : '/media/no-key.webp'}
            alt={hasApiKey ? t('appName') : t('odsBalanceNoKey')}
            draggable={false}
          />
          {hasApiKey ? null : (
            <button
              type="button"
              className={styles.keyButton}
              onClick={() => openSettings('data')}
            >
              {t('odsWelcomeAddKey')}
            </button>
          )}
        </div>
        <ChatInput sessionId={null} />
        {isMobile ? <div className={styles.caveat}>{t('contentCaveat')}</div> : null}
      </div>
    </div>
  )
}
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("Welcome ok")

# ---------- 4. Welcome 样式 ----------
p = root / "src/components/session/Welcome.module.css"
t = io.open(p, encoding="utf-8").read()
if ".mascot" not in t:
    t = t.replace(
        """.greeting {""",
        """.mascot {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  margin: 0 0 21px;
}

.mascotImage {
  width: min(300px, 62vw);
  max-height: 36vh;
  object-fit: contain;
  /* 图片本身是白底，圆角一下更像贴纸 */
  border-radius: 16px;
  user-select: none;
  -webkit-user-drag: none;
}

.keyButton {
  border: none;
  border-radius: 100px;
  padding: 10px 22px;
  background-color: var(--dsw-alias-button-primary-fill);
  color: var(--dsw-static-neutral-bluish-00);
  font: inherit;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
}

.greeting {""",
        1,
    )
    t = t.replace(
        """  .greeting {
    flex-shrink: 0;
    margin: auto 0;
  }""",
        """  .mascot {
    flex-shrink: 0;
    margin: auto 0 12px;
  }

  .mascotImage {
    width: min(240px, 56vw);
    max-height: 30vh;
  }

  .greeting {
    flex-shrink: 0;
    margin: auto 0;
  }""",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("Welcome css ok")

# ---------- 5. 侧栏品牌换 logo ----------
p = root / "src/components/sider/Sider.tsx"
t = io.open(p, encoding="utf-8").read()
old = """        <div className={styles.appName}>{t('appName')}</div>"""
new = """        <div className={styles.brand}>
          <img className={styles.brandLogo} src="/media/logo-128.webp" alt="" draggable={false} />
          <div className={styles.appName}>{t('appName')}</div>
        </div>"""
if old in t:
    t = t.replace(old, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("Sider ok")

# ---------- 6. i18n ----------
zh = [("odsWelcomeAddKey", "还差一个 API Key → 去设置")]
p = root / "src/i18n/zh.ts"
t = io.open(p, encoding="utf-8").read()
if "odsWelcomeAddKey" not in t:
    t = t.replace("} as const", "  odsWelcomeAddKey: '还差一个 API Key → 去设置',\n} as const", 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("zh ok")

p = root / "src/i18n/en.ts"
t = io.open(p, encoding="utf-8").read()
if "odsWelcomeAddKey" not in t:
    t = t.replace(
        "} satisfies Record<keyof typeof zh, string>",
        "  odsWelcomeAddKey: 'Add an API key to start',\n} satisfies Record<keyof typeof zh, string>",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("en ok")
