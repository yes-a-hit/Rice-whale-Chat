import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 18:52）

### 图片全部转 WEBP

`notes/to_webp.py`（质量 82、method 6，RGBA 保 alpha）：

```
hungry.png   77 KB -> hungry.webp   51 KB
logo-128.png 12 KB -> logo-128.webp  3 KB
tech-mascot  510 KB -> 90 KB
wait.png     57 KB -> wait.webp     49 KB
welcome.png  88 KB -> welcome.webp  60 KB
maid-mascot  新     -> 57 KB
```

`dist/media` 总计 856 KB → 312 KB。组件引用全部改成 `.webp`（`Welcome` / `Sider` / `Onboarding` / `AssistantMessage`）。

### 主题体系

`src/app/themes/{types,registry}.ts` + `themes.css`，取代原 `skins.ts` 的 5 套配色（旧 id 自动回落 `plain`）。

- 七个内置：`plain` 最简 / `ink` 国风 / `maid` 经典女仆 / `tech` 科技 / `sumi` 水墨 / `moon` 月兔 / `gyu` 奶牛。
- 装饰走 `--ods-decor` 变量，由 `App.module.css` 的 `.frame` 拼到 `background-image` —— 不插 DOM、不挡点击。
- 自动匹配 `matchTheme()`：先比 `models` 再比 `hosts`，子串匹配，不写正则。当前只拿得到 `apiBaseUrl`，所以用 host 判断：`moonshot` → 月兔，`bigmodel`/`zhipu` → 奶牛。
- 设置项 `themeAuto`（默认关）；`selectTheme()` 里手动选择优先。
- 素材：`maid-mascot.webp` 由 `logo.png` 去白底生成；`tech-mascot.webp` 由 `tech-plus.jpg` 裁上半身 + 阈值抠深色背景生成。`moon`/`gyu` 暂无立绘，回落到默认图。
- 文档：`docs/themes.md`（配色变量清单、四步新增法、匹配规则、稳定性契约）。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 通过。截图：`notes/theme-tech.png`、`theme-maid.png`、`theme-sumi.png`。
产物 `android/app/build/outputs/apk/release/app-release.apk`（`com.ricewhale.chat`，v1.0.0-alpha.1）。

### 仍未完成

- 月兔、奶牛两套主题缺立绘（水兔女郎 / 萝莉牛娘），素材槽已留
- 本地 NPU 生图与本地 TTS 只有接口，需要原生插件
- 真机实测

## 构建
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status + "\n- 调试：`pnpm android:apk`\n- 正式：`pnpm android:release`\n")
print("audit ok")
