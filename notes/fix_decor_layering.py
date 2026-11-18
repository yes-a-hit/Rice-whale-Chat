import io
import re
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. themes.css：只留图片，遮罩交给 .frame ----------
p = root / "src/app/themes/themes.css"
t = io.open(p, encoding="utf-8").read()

t = re.sub(
    r"--ods-decor: linear-gradient\([^)]*\),\s*\n\s*url\('\./assets/(decor-[a-z]+\.webp)'\);",
    r"--ods-image: url('./assets/\1');",
    t,
)
# 夜间特殊遮罩段整段删掉（改由统一变量控制）
t = re.sub(
    r"\n/\* 夜间模式：[\s\S]*?url\('\./assets/decor-gyu\.webp'\);\n\}\n",
    "\n",
    t,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("themes.css ok")
print("ods-image count:", t.count("--ods-image"))

# ---------- 2. .frame：遮罩 + 图 ----------
p = root / "src/app/App.module.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "  background-image: var(--ods-decor, none);",
    "  /* 遮罩层用 body 上的 --ods-veil-*（夜间会换成深色），下面才是主题底图 */\n"
    "  background-image: linear-gradient(var(--ods-veil-1), var(--ods-veil-2)), var(--ods-image, none);",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("frame ok")
