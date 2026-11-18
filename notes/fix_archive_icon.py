import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\sider\SessionItem.tsx")
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "import { IconEditOutline16, IconEllipsisOutline16, IconTrashOutline16 } from '../base/icons.js'",
    "import {\n  IconEditOutline16,\n  IconEllipsisOutline16,\n  IconFolderOutline16,\n  IconTrashOutline16,\n} from '../base/icons.js'",
    1,
)
t = t.replace(
    """              label: session.archived ? t('odsUnarchive') : t('odsArchive'),""",
    """              label: session.archived ? t('odsUnarchive') : t('odsArchive'),
              icon: <IconFolderOutline16 />,""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
