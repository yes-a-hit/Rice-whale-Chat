import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- docs 更新 ----------
p = root / "docs/themes.md"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """### 第二步：背景装饰（可选）

在同一个选择器里加一行 `--ods-decor`，它的值会被拼到 `.frame` 的 `background-image` 上：

```css
  --ods-decor: radial-gradient(120% 60% at 12% -10%, rgba(75, 90, 196, 0.16), transparent 60%);
```

可以叠多层渐变（见 `tech` 主题的网格写法）。装饰只是背景，**不占 DOM、不接事件、不会挡点击**。""",
    """### 第二步：背景装饰（可选）

在同一个选择器里加一行 `--ods-image`，`App.module.css` 的 `.frame` 会把它拼成

```css
background-image: linear-gradient(var(--ods-veil-1), var(--ods-veil-2)), var(--ods-image, none);
```

第一层是遮罩：`--ods-veil-1/2` 定义在 `:root`（白）与 `body[data-ds-dark-theme='dark']`（近黑）两处，
所以**同一张图在深色模式下自动换成深色遮罩**，不用为主题单独写夜间样式。

图像放在 `src/app/themes/assets/decor-<id>.webp`，CSS 里用相对路径 `url('./assets/...')`
（写 `/media/...` 会被打包器当模块解析并报错）。装饰只是背景，**不占 DOM、不接事件、不挡点击**。""",
    1,
)

if "### 立绘" not in t:
    t = t.replace(
        """### 第四步：注册""",
        """### 第三步补充：立绘

每套主题一张 `<id>-mascot.webp`（透明底，宽 620 左右），注册在 `assets.welcome`。
角色本身不带文字——欢迎语由 DOM 气泡渲染（`odsWelcomeBubble`，默认「欢迎回来，想从哪里开始」），
这样换语言、换措辞都不用重出图。

### 第四步：注册""",
        1,
    )

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("docs ok")

# ---------- gitignore 原图 ----------
p = root / ".gitignore"
t = io.open(p, encoding="utf-8").read()
if "notes/src-art" not in t:
    t = t.rstrip() + "\n# 出图原稿（4MB+，需要时重新跑 notes/run_mascot.py）\nnotes/src-art/\n"
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("gitignore ok")
