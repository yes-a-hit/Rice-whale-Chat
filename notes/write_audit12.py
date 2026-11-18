import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 20:45）

### 主题：立绘归属、欢迎语、夜间适配（m02581 / m02587）

**「换主题没用」的真因**：三处叠加 —— ① plain 与 ink 的主色都是青蓝，色相几乎一样；
② 装饰图的白色遮罩 0.84 把纹理压到看不见；③ 立绘七套里五套共用同一张。
所以换了主题视觉上确实没变化。

修法：

- **配色拉开**：plain 保持官方紫蓝（不设变量），ink 青绿 `#2f7d84`，maid 深藏蓝 `#3b4f8a`，
  tech 亮青 `#0093c4`，sumi 墨灰 `#4a4a48`，moon 紫 `#8a6fd6`，gyu 蓝灰 `#4a6f8f`。
- **遮罩下调**到 0.78–0.90，纹理可见。
- **每主题专属立绘**：用 moss 出 5 张白底立绘（`notes/run_mascot.py`，832×1216，10 步），
  再走 `notes/make_theme_mascots.py` 抠白 → `figure/out/<id>-mascot.webp`（57–93 KB）。
  - ink 汉服鲸鱼女仆 / plain 现代白卫衣 / sumi 黑色和服 / moon 月兔 / gyu 奶牛娘
  - 旧的 `welcome.webp`（汉服 + 烧在图里的气泡）退役删除，`hungry.webp` 保留共用
- **欢迎语改 DOM 气泡**：`Welcome.tsx` 里 `<div className={styles.bubble}>{t('odsWelcomeBubble')}</div>`，
  CSS 定位在图左上（`top: 10%`，`max-width: 44%`），带指向角色的小三角。
  i18n key 默认「欢迎回来，\\n想从哪里开始」，换语言/措辞不用重出图。
- **夜间适配**：原来遮罩是写死的白色，深色模式下整屏发白。改成
  - `:root { --ods-veil-1/2: 白 }`、`body[data-ds-dark-theme='dark'] { --ods-veil-1/2: 近黑 }`
  - 主题只声明 `--ods-image: url(...)`，遮罩由 `.frame` 拼：`linear-gradient(var(--ods-veil-1), var(--ods-veil-2)), var(--ods-image, none)`
  - 关键教训：CSS 变量在**声明它的元素**上求值。`--ods-decor` 若写在 `html` 上，
    `var(--ods-veil)` 就按 html 的值算，body 上的夜间覆盖不参与。拆成两层后各自在自己的层求值才对。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 通过。APK 47.92MB。
浅色截图：`notes/t-ink.png`、`t-plain.png`、`t-moon.png`、`t-gyu.png`、`t-sumi.png`；
夜间截图：`notes/v-ink-dark.png`、`td-gyu.png`、`td-moon.png`、`td-sumi.png`。
`dist/media` 合计 630 KB（10 个 webp）。

### 仍未完成

- NPU 上真跑模型（模型转换 + 中文 G2P）
- 上下文压缩
- 真机实测（NPU 检测、主题切换、夜间模式）

## 构建
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status + "\n- 调试：`pnpm android:apk`\n- 正式：`pnpm android:release`\n")
print("audit ok")
