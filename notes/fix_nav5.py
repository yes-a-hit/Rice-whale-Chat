import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# tab 用短名，页内标题才是全称
p = root / "src/i18n/zh.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace("odsLabSection: '实验性玩法',", "odsLabSection: '实验',")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)

# 五个 tab 收窄
p = root / "src/components/settings/Settings.module.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """    gap: 6px;
    width: auto;
    min-width: 86px;
    margin: 0;
    padding: 9px 8px;""",
    """    gap: 5px;
    width: auto;
    min-width: 70px;
    margin: 0;
    padding: 9px 7px;
    font-size: 13px;""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("nav ok")
