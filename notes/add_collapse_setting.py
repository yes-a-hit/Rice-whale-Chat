import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- A. 思考自动折叠 ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
if "collapseThinking" not in t:
    t = t.replace(
        "  showBalance: boolean",
        "  showBalance: boolean\n  /** 思考内容完成后自动收起 */\n  collapseThinking: boolean",
        1,
    )
    t = t.replace(
        "  showBalance: read(KEYS.showBalance) !== 'false',",
        "  showBalance: read(KEYS.showBalance) !== 'false',\n  collapseThinking: read(KEYS.collapseThinking) === 'true',",
        1,
    )
    t = t.replace(
        "  showBalance: 'ods:show-balance',",
        "  showBalance: 'ods:show-balance',\n  collapseThinking: 'ods:collapse-thinking',",
        1,
    )
    t = t.replace(
        "export const setShowBalance = ",
        "export const setCollapseThinking = (collapseThinking: boolean) => {\n"
        "  write(KEYS.collapseThinking, collapseThinking ? 'true' : 'false')\n"
        "  useSettings.setState({ collapseThinking })\n"
        "}\n\n"
        "export const setShowBalance = ",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("settings collapseThinking ok")
