import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\settings\SettingsDialog.tsx")
t = io.open(p, encoding="utf-8").read()
if "DataSection } from" not in t:
    t = t.replace(
        "import { ExtSettings } from './ExtSettings.js'",
        "import { DataSection } from './DataSection.js'\nimport { ExtSettings } from './ExtSettings.js'",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("import added")
else:
    print("already there")
