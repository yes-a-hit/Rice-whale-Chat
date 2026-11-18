import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- settings：themeAuto 字段 ----------
p = root / "src/services/settings.ts"
t = io.open(p, encoding="utf-8").read()
if "themeAuto" not in t:
    t = t.replace(
        "  skin: string",
        "  skin: string\n  /** 跟随接口自动换主题（kimi → 月兔，glm → 奶牛） */\n  themeAuto: boolean",
        1,
    )
    t = t.replace(
        "  skin: 'ods:skin',",
        "  skin: 'ods:skin',\n  themeAuto: 'ods:theme-auto',",
        1,
    )
    t = t.replace(
        "  skin: read(KEYS.skin) ?? 'deepseek',",
        "  skin: read(KEYS.skin) ?? 'plain',\n  themeAuto: read(KEYS.themeAuto) === 'true',",
        1,
    )
    t = t.replace(
        "export const setSkin =",
        """export const setThemeAuto = (themeAuto: boolean) => {
  write(KEYS.themeAuto, String(themeAuto))
  useSettings.setState({ themeAuto })
}

export const setSkin =""",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("settings themeAuto ok")

# ---------- main.tsx：换样式表 ----------
p = root / "src/main.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("'./app/skins.css'", "'./app/themes/themes.css'")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("main css ok")

# ---------- 删除旧 skins.css ----------
old = root / "src/app/skins.css"
if old.exists():
    old.unlink()
    print("old skins.css removed")
