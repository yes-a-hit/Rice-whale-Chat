import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\services\settings.ts")
t = io.open(p, encoding="utf-8").read()

# 导入 ChatModel / CHAT_MODELS / DEFAULT_CHAT_MODEL
if "CHAT_MODELS" not in t.split("export const useSettings")[0]:
    first_import = t.index("import ")
    t = (
        t[:first_import]
        + "import {\n  CHAT_MODELS,\n  DEFAULT_CHAT_MODEL,\n  type ChatModel,\n} from './api/types.js'\n"
        + t[first_import:]
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("import ok")
else:
    print("import exists")
