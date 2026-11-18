import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 科技网格加深一点，白底上才看得出来
p = root / "src/app/themes/themes.css"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """  --ods-decor: linear-gradient(rgba(0, 144, 200, 0.07) 1px, transparent 1px) 0 0 / 100%
      28px,
    linear-gradient(90deg, rgba(0, 144, 200, 0.07) 1px, transparent 1px) 0 0 / 28px 100%,
    radial-gradient(90% 50% at 80% 0%, rgba(18, 174, 232, 0.18), transparent 60%);""",
    """  --ods-decor: linear-gradient(rgba(0, 144, 200, 0.12) 1px, transparent 1px) 0 0 / 100%
      28px,
    linear-gradient(90deg, rgba(0, 144, 200, 0.12) 1px, transparent 1px) 0 0 / 28px 100%,
    radial-gradient(90% 50% at 80% 0%, rgba(18, 174, 232, 0.2), transparent 60%);""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("tech grid ok")

# README：主题一节
p = root / "README.md"
t = io.open(p, encoding="utf-8").read()
section = """## 主题

设置 → 扩展 → 主题。七个内置：

| 主题 | 风格 |
|---|---|
| 最简（原版） | 官方蓝，无装饰 |
| 国风 | 青蓝水墨，鲸鱼娘立绘 |
| 经典女仆 | 深蓝白蕾丝斜纹，女仆装 |
| 科技 | 青蓝荧光网格，机能风 |
| 水墨 | 墨色留白，大面积晕染 |
| 月兔（Kimi） | 米白淡紫，月晕 |
| 奶牛（GLM） | 黑白斑点 |

**跟随接口自动换主题**：打开后，服务地址含 `moonshot` 自动切月兔，含 `bigmodel` 自动切奶牛。
手动选择优先于自动。

主题是可扩展的：加一段 CSS 变量 + 一条注册项就行，格式与社区约定见 [docs/themes.md](docs/themes.md)。

## 实验性玩法"""
t = t.replace("## 实验性玩法", section, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("README themes ok")
