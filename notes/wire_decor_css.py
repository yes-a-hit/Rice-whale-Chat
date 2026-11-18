import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\app\themes\themes.css")
t = io.open(p, encoding="utf-8").read()

# 每套主题的 --ods-decor 换成「白色遮罩 + 实际底图」，图片只留一层淡淡的纹理
repl = {
    "ink": """  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.84), rgba(255, 255, 255, 0.9)),
    url('/media/decor-ink.webp');""",
    "maid": """  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.94)),
    url('/media/decor-maid.webp');""",
    "tech": """  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0.92)),
    url('/media/decor-tech.webp');""",
    "sumi": """  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.82), rgba(255, 255, 255, 0.9)),
    url('/media/decor-sumi.webp');""",
    "moon": """  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.92)),
    url('/media/decor-moon.webp');""",
    "gyu": """  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0.93)),
    url('/media/decor-gyu.webp');""",
}

lines = t.split("\n")
current = None
out = []
skip_depth = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith("html[data-theme="):
        current = stripped.split("'")[1]
        out.append(line)
        continue
    if stripped.startswith("--ods-decor:"):
        if current in repl:
            out.append(repl[current])
            skip_depth = 2  # 该变量占 2 行（第一行 + 续行），后续续行要跳过
        else:
            out.append(line)
        continue
    if skip_depth > 0 and stripped and not stripped.startswith("--"):
        skip_depth -= 1
        continue
    skip_depth = 0
    out.append(line)

t = "\n".join(out)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("themes.css decor swapped")

# .frame 让底图铺满
p = pathlib.Path(r"E:\flutter\open-deepseek\src\app\App.module.css")
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """  background-image: var(--ods-decor, none);
  background-attachment: local;""",
    """  background-image: var(--ods-decor, none);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: local;""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("frame size ok")
