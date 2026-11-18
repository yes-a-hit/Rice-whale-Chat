import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# Sider：在第一个 useTranslate 后插入 logo
p = root / "src/components/sider/Sider.tsx"
t = io.open(p, encoding="utf-8").read()
if "const logo =" not in t:
    t = t.replace(
        "  const t = useTranslate()",
        "  const t = useTranslate()\n  const logo = themeAsset(useSettings(selectTheme), 'logo')",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("sider inserted")

# Onboarding：补 useSettings 导入
p = root / "src/components/onboarding/Onboarding.tsx"
t = io.open(p, encoding="utf-8").read()
if "useSettings" not in t.split("export const Onboarding")[0]:
    t = t.replace(
        "import { selectTheme } from '../../app/skins.js'",
        "import { selectTheme } from '../../app/skins.js'\nimport { useSettings } from '../../services/settings.js'",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("onboarding import ok")
