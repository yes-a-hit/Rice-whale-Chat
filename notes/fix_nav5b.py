import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\settings\Settings.module.css")
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """    gap: 5px;
    width: auto;
    min-width: 70px;
    margin: 0;
    padding: 9px 7px;
    font-size: 13px;""",
    """    gap: 4px;
    width: auto;
    min-width: 62px;
    margin: 0;
    padding: 9px 6px;
    font-size: 12.5px;""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("nav5 ok")
