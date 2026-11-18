import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. types：主题加调色板与装饰图 ----------
p = root / "src/app/themes/types.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """export type Theme = {
  id: ThemeId""",
    """/**
 * 主色阶：只覆盖 `--dsw-static-blue-50..900`。
 * 用 TS 而不是纯 CSS 存放，是因为套用时要写成行内变量——
 * 行内样式优先级最高，不会被主题选择器匹配不到的情况坑掉。
 */
export type ThemePalette = Record<
  '50' | '100' | '200' | '300' | '400' | '450' | '500' | '600' | '800' | '900',
  string
>

export type Theme = {
  /** 主色阶；省略表示沿用官方配色（plain） */
  palette?: ThemePalette
  /** 装饰底图文件名，位于 /media/；省略表示无装饰 */
  image?: string
  id: ThemeId""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("types ok")
