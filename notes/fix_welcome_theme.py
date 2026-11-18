import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\session\Welcome.tsx")
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    "import { useSettings } from '../../services/settings.js'",
    "import { useSettings } from '../../services/settings.js'\n"
    "import { selectTheme } from '../../app/skins.js'\n"
    "import { themeAsset } from '../../app/themes/registry.js'",
    1,
)
t = t.replace(
    "  const hasApiKey = useSettings((state) => Boolean(state.apiKey))",
    "  const hasApiKey = useSettings((state) => Boolean(state.apiKey))\n"
    "  const theme = useSettings(selectTheme)",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("welcome ok")
