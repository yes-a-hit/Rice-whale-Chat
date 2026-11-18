import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 内容区右侧负边距在移动端导致按钮贴边裁切 ----------
p = root / "src/components/settings/Settings.module.css"
t = io.open(p, encoding="utf-8").read()
old = """  .content {
    padding-top: 16px;
    padding-left: 0;
    padding-right: 4px;"""
new = """  .content {
    margin-right: 0;
    padding-top: 16px;
    padding-left: 0;
    padding-right: 4px;"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("css content margin ok")

# ---------- 2. 移动端顶栏加设置入口 ----------
p = root / "src/components/session/MobileHeader.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { IconMenuOutline20, IconNewChatOutline20 } from '../base/icons.js'",
    "import { IconMenuOutline20, IconNewChatOutline20, IconSettingsOutline16 } from '../base/icons.js'",
    1,
)
t = t.replace(
    "import { openMobileSider } from '../sider/mobileSiderState.js'",
    "import { openMobileSider } from '../sider/mobileSiderState.js'\n"
    "import { openSettings } from '../settings/settingsDialogState.js'",
    1,
)
old = """      {title === undefined ? null : (
        <>
          <div className={styles.title}>{title}</div>
          <IconButton
            size="xl"
            tone="primary"
            icon={<IconNewChatOutline20 />}
            aria-label={t('newChat')}
            onClick={newChat}
          />
        </>
      )}"""
new = """      {title === undefined ? null : (
        <>
          <div className={styles.title}>{title}</div>
          <IconButton
            size="xl"
            tone="primary"
            icon={<IconNewChatOutline20 />}
            aria-label={t('newChat')}
            onClick={newChat}
          />
        </>
      )}
      {/* 手机上唯一的常驻设置入口：任何页面都能进 */}
      <IconButton
        size="xl"
        tone="primary"
        icon={<IconSettingsOutline16 />}
        aria-label={t('settings')}
        onClick={() => openSettings('general')}
      />"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("mobile header ok")

# ---------- 3. 删除位置信息设置 ----------
p = root / "src/components/settings/SettingsDialog.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("""              <ThemeSetting />
              <LocaleSetting />
              <TtsVoiceSetting />
              <LocationSetting />""", """              <ThemeSetting />
              <LocaleSetting />
              <TtsVoiceSetting />""", 1)
# 删掉 LocationSetting 组件定义（从注释开始到下一个组件注释）
start = t.find("const LocationSetting = () => {")
if start != -1:
    # 往前找该组件上方的注释起点
    doc_start = t.rfind("/**", 0, start)
    # 往后找组件结束：下一个 "\nconst " 或 "\n/**"
    next_fn = t.find("\nconst ", start)
    next_doc = t.find("\n/**", start)
    end = min(x for x in (next_fn, next_doc, len(t)) if x > start)
    removed = t[doc_start if doc_start != -1 else start:end]
    assert "LocationSetting" in removed and len(removed) < 4000
    t = t[: (doc_start if doc_start != -1 else start)] + t[end:]
    print("removed LocationSetting", len(removed), "chars")
# 清理未使用的导入
t = t.replace("import { regionCodes, getRegionName, provinces } from '../../services/location.js'\n", "")
t = t.replace("  setLocation,\n", "")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settings dialog location removed")
