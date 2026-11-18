import io
import pathlib
import re

p = pathlib.Path(r"E:\flutter\open-deepseek\src\app\themes\themes.css")
t = io.open(p, encoding="utf-8").read()

# 配色与 --ods-image 已经搬到 registry.ts（行内变量），这里只留遮罩与说明
head = """/*
 * 主题样式：只保留结构性部分（遮罩色）。
 *
 * 各主题的主色阶与装饰图在 `src/app/themes/registry.ts` 里，
 * 套用时由 `src/app/skins.ts` 写成行内变量——行内样式优先级最高，
 * 不依赖 `html[data-theme='x']` 选择器能否匹配上。
 *
 * 这里只定义遮罩：浅色模式白、深色模式近黑，`.frame` 会拼成
 * `linear-gradient(--ods-veil-1, --ods-veil-2), var(--ods-image)`。
 */

:root {
  --ods-veil-1: rgba(255, 255, 255, 0.78);
  --ods-veil-2: rgba(255, 255, 255, 0.9);
}

body[data-ds-dark-theme='dark'] {
  --ods-veil-1: rgba(12, 14, 20, 0.82);
  --ods-veil-2: rgba(12, 14, 20, 0.92);
}
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head)
print("themes.css reduced")
