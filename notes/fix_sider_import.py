import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\sider\Sider.tsx")
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { IconPanelLeftOutline16, IconSettingsOutline16, NewChatIcon } from '../base/icons.js'",
    "import {\n  IconFolderOutline16,\n  IconPanelLeftOutline16,\n  IconSettingsOutline16,\n  NewChatIcon,\n} from '../base/icons.js'",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
