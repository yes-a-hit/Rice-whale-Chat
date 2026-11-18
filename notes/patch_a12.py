import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- icons.tsx 追加图片图标 ----------
p = root / "src/components/base/icons.tsx"
t = io.open(p, encoding="utf-8").read()
if "IconImageOutline16" not in t:
    t += """
export const IconImageOutline16 = () => (
  <svg width={16} height={16} viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="2" y="2.75" width="12" height="10.5" rx="1.75" stroke="currentColor" strokeWidth="1.3" />
    <circle cx="5.9" cy="6" r="1.05" fill="currentColor" />
    <path
      d="M3.2 12.2l3.1-3.4 2.3 2.1 1.9-1.9 2.3 3.2"
      stroke="currentColor"
      strokeWidth="1.3"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
)
"""
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("icons ok")

# ---------- ChatInput 接入生图入口（仅 Plus 模式） ----------
p = root / "src/components/chatInput/ChatInput.tsx"
t = io.open(p, encoding="utf-8").read()
assert "IconImageOutline16" not in t

t = t.replace(
    "  IconSendOutline16,",
    "  IconImageOutline16,\n  IconSendOutline16,",
    1,
)
t = t.replace(
    "import { IconButton } from '../base/IconButton.js'",
    "import { IconButton } from '../base/IconButton.js'\n"
    "import { openImageDialog } from '../image/imageDialogState.js'\n"
    "import { useSettings } from '../../services/settings.js'",
    1,
)

old = """        <div className={styles.right}>
          <VoiceButton"""
new = """        <div className={styles.right}>
          {useSettings((state) => state.uiMode) === 'plus' ? (
            <IconButton
              size="m"
              tone="primary"
              icon={<IconImageOutline16 />}
              tooltip={t('odsImageDialogTitle')}
              onClick={openImageDialog}
            />
          ) : null}
          <VoiceButton"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ChatInput ok")

# ---------- App 挂载生图弹窗 ----------
p = root / "src/app/App.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { Onboarding } from '../components/onboarding/Onboarding.js'",
    "import { Onboarding } from '../components/onboarding/Onboarding.js'\nimport { ImageDialog } from '../components/image/ImageDialog.js'",
    1,
)
old = """      {onboarded ? null : <Onboarding />}"""
new = """      <ImageDialog />
      {onboarded ? null : <Onboarding />}"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("App ok")
