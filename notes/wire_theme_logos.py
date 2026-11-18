import io
import pathlib
import re

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. types: builtinBubble ----------
p = root / "src/app/themes/types.ts"
t = io.open(p, encoding="utf-8").read()
if "builtinBubble" not in t:
    t = t.replace(
        "  /** 装饰底图文件名，位于 /media/；省略表示无装饰 */",
        "  /** 立绘自带气泡文字（老素材），为真时不再渲染 DOM 气泡 */\n  builtinBubble?: boolean\n  /** 装饰底图文件名，位于 /media/；省略表示无装饰 */",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("types ok")

# ---------- 2. registry: 每主题自己的 logo ----------
p = root / "src/app/themes/registry.ts"
t = io.open(p, encoding="utf-8").read()
t = re.sub(r"      logo: 'logo-128\.webp',", lambda m: m.group(0), t)  # no-op anchor
for theme in ("plain", "ink", "maid", "tech", "sumi", "moon", "gyu"):
    marker = f"    id: '{theme}',"
    index = t.find(marker)
    assert index >= 0, theme
    end = t.find("  },", index)
    block = t[index:end]
    new_block = block.replace(
        "      logo: 'logo-128.webp',", f"      logo: '{theme}-logo.webp',"
    )
    t = t[:index] + new_block + t[end:]

# ink 的立绘自带气泡
t = t.replace(
    """    // 汉服鲸鱼女仆是国风的主角
    assets: {
      welcome: 'ink-mascot.webp',""",
    """    // 汉服鲸鱼女仆是国风的主角；这张老图自带气泡文字
    builtinBubble: true,
    assets: {
      welcome: 'ink-mascot.webp',""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("registry ok")

# ---------- 3. Sider / Onboarding 用主题 logo ----------
p = root / "src/components/sider/Sider.tsx"
t = io.open(p, encoding="utf-8").read()
if "themeAsset" not in t:
    t = t.replace(
        'src="/media/logo-128.webp"',
        "src={logo}",
        1,
    )
    t = t.replace(
        "import styles from './Sider.module.css'",
        "import { selectTheme } from '../../app/skins.js'\n"
        "import { themeAsset } from '../../app/themes/registry.js'\n"
        "import { useSettings } from '../../services/settings.js'\n"
        "import styles from './Sider.module.css'",
        1,
    )
    # 在组件内取 logo
    t = re.sub(
        r"(export const Sider = memo\(function Sider\([\s\S]{0,400}?\) \{\n)",
        r"\1  const logo = themeAsset(useSettings(selectTheme), 'logo')\n",
        t,
        count=1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("sider ok")

p = root / "src/components/onboarding/Onboarding.tsx"
t = io.open(p, encoding="utf-8").read()
if "themeAsset" not in t:
    t = t.replace('src="/media/logo-128.webp"', "src={logo}", 1)
    t = t.replace(
        "import styles from './Onboarding.module.css'",
        "import { selectTheme } from '../../app/skins.js'\n"
        "import { themeAsset } from '../../app/themes/registry.js'\n"
        "import styles from './Onboarding.module.css'",
        1,
    )
    t = re.sub(
        r"(export const Onboarding = \(\) => \{\n)",
        r"\1  const logo = themeAsset(useSettings(selectTheme), 'logo')\n",
        t,
        count=1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("onboarding ok")

# ---------- 4. Welcome: builtinBubble 时不渲染 DOM 气泡 ----------
p = root / "src/components/session/Welcome.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "          {hasApiKey ? <div className={styles.bubble}>{t('odsWelcomeBubble')}</div> : null}",
    "          {hasApiKey && !themeById(theme).builtinBubble ? (\n"
    "            <div className={styles.bubble}>{t('odsWelcomeBubble')}</div>\n"
    "          ) : null}",
    1,
)
t = t.replace(
    "import { themeAsset } from '../../app/themes/registry.js'",
    "import { themeAsset, themeById } from '../../app/themes/registry.js'",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("welcome ok")
