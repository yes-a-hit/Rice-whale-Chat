import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 19:34）

### 主题装饰底图（moss 出图）

用本机 ComfyUI + moss 模型批量出了六张装饰底图，`notes/run_moss.py` 驱动：

| 主题 | 图 | 体积 |
|---|---|---|
| ink | 山水薄雾 + 竹叶 | 19 KB |
| maid | 蕾丝边框 + 蝴蝶结 | 19 KB |
| tech | 青蓝电路 HUD | 14 KB |
| sumi | 毛笔 + 墨点 | 14 KB |
| moon | 紫夜大月亮 | 13 KB |
| gyu | 奶油底黑斑 | 4 KB |

出图参数：1024×1024 → 缩 640、WEBP q80；8 步采样（25 步在 8G 显存上要 offload 太久）。

接线方式：图放 `src/app/themes/assets/decor-<id>.webp`，CSS 里

```css
--ods-decor: linear-gradient(rgba(255,255,255,0.86), rgba(255,255,255,0.92)),
  url('./assets/decor-tech.webp');
```

第一层白色遮罩把底图压到「隐约可见」，透明度按图案强度分档（0.82 山水 / 0.86–0.90 通用 / 0.93–0.97 高对比）。
`App.module.css` 的 `.frame` 加了 `background-size: cover; background-position: center`。

**踩坑**：CSS 里写 `url('/media/x.webp')` 会被 rspack 当模块解析并报 `Module not found`。
改放源码目录用相对路径，让打包器处理并加 hash。

**踩坑**：ComfyUI 默认只读自己的 `models/`，Comfy Desktop 的模型在 `E:\\Comfy-Desktop\\ComfyUI-Shared\\models`。
写了 `extra_model_paths.yaml` 并用 `--extra-model-paths-config` 启动才认。另外 workflow 里写的
`moss_image_sft_deband_int8_convrot` / `qwen3.5_9b_int8_convrot` / `flux2-vae` 本机没有，
实际用的是 `moss_image_sft_turbo_int8_convrot` / `qwen3.5_9b_w4a8_gptq` / `flux2-vae_small`。

工作流存档：`notes/moss-decor-workflow.json`；文档：`docs/themes.md` 第 6 节。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 通过。APK 6.72MB。
截图：`notes/dc-ink.png`、`dc-tech.png`、`dc-sumi.png`、`dc-maid.png`、`dc-moon.png`、`de-gyu.png`。

### 仍未完成

- 月兔/奶牛专属立绘（装饰有了，人物还是国风那张）
- 上下文压缩本身
- 本地 NPU 生图与本地 TTS 只有接口
- 真机实测

## 构建
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status + "\n- 调试：`pnpm android:apk`\n- 正式：`pnpm android:release`\n")
print("audit ok")
