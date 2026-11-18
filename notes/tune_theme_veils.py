import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 1. moon / gyu 底图对比度偏高，单独加深遮罩
p = root / "src/app/themes/themes.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """  --ods-decor: linear-gradient(var(--ods-veil-1), var(--ods-veil-2)),
    url('./assets/decor-moon.webp');""",
    """  /* 月晕边缘偏硬，遮罩再压一点 */
  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.95)),
    url('./assets/decor-moon.webp');""",
    1,
)
t = t.replace(
    """  --ods-decor: linear-gradient(var(--ods-veil-1), var(--ods-veil-2)),
    url('./assets/decor-gyu.webp');""",
    """  /* 黑斑对白底太跳，压到只剩纸纹 */
  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.93), rgba(255, 255, 255, 0.97)),
    url('./assets/decor-gyu.webp');""",
    1,
)

# 2. 夜间覆盖：data-theme 在 html、data-ds-dark-theme 在 body，选择器要从 html 往下写
if "html[data-theme='gyu'] body[data-ds-dark-theme" not in t:
    t = t.rstrip() + """

/* 夜间模式：个别主题的遮罩要换深色，不然整屏发白 */
html[data-theme='moon'] body[data-ds-dark-theme='dark'] {
  --ods-decor: linear-gradient(rgba(14, 12, 20, 0.86), rgba(14, 12, 20, 0.94)),
    url('./assets/decor-moon.webp');
}

html[data-theme='gyu'] body[data-ds-dark-theme='dark'] {
  --ods-decor: linear-gradient(rgba(16, 16, 18, 0.9), rgba(16, 16, 18, 0.96)),
    url('./assets/decor-gyu.webp');
}
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("themes.css tuned")

# 3. 气泡下移
p = root / "src/components/session/Welcome.module.css"
t = io.open(p, encoding="utf-8").read()
if "  top: 6%;" in t:
    t = t.replace("  top: 6%;", "  top: 10%;", 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("bubble pos ok")
