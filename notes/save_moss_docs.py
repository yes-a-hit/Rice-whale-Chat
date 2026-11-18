import io
import json
import pathlib
import shutil

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 保存一份可复现的 moss 工作流（已改成实际用到的模型名）
src = pathlib.Path(r"C:\Users\doubl\Downloads\moss_deband_int8_api.json")
workflow = json.load(io.open(src, encoding="utf-8"))["prompt"]
workflow["3"]["inputs"]["unet_name"] = "moss_image_sft_turbo_int8_convrot.safetensors"
workflow["4"]["inputs"]["clip_name"] = "qwen3.5_9b_w4a8_gptq.safetensors"
workflow["5"]["inputs"]["vae_name"] = "flux2-vae_small.safetensors"
workflow["9"]["inputs"]["expression"] = "8"
target = root / "notes" / "moss-decor-workflow.json"
io.open(target, "w", encoding="utf-8", newline="\n").write(
    json.dumps({"prompt": workflow}, ensure_ascii=False, indent=2)
)
print("workflow saved", target.stat().st_size // 1024, "KB")

# docs 补装饰图章节
p = root / "docs" / "themes.md"
t = io.open(p, encoding="utf-8").read()
addition = """
---

## 6. 装饰底图（decor）

每套主题可以带一张背景纹理，放在 `src/app/themes/assets/decor-<id>.webp`（1024 见方出图，缩到 640 再存，约 4–20 KB）。

CSS 里这样用：

```css
  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0.92)),
    url('./assets/decor-tech.webp');
```

第一层是白色遮罩，把底图压到「隐约可见」。**遮罩透明度就是这个主题的气质**：

| 透明度 | 观感 | 适合 |
|---|---|---|
| 0.80–0.85 | 纹理明显 | 山水、墨迹这种本来就淡的图 |
| 0.86–0.90 | 隐约 | 大多数主题 |
| 0.92–0.97 | 几乎只是纸纹 | 高对比图案（奶牛斑、电路） |

低于 0.78 就开始影响文字对比度了，别越线。

### 出图

本机用 ComfyUI + moss 模型批量出，脚本 `notes/run_moss.py`：

```bash
python notes/run_moss.py            # 全部主题
python notes/run_moss.py ink tech   # 指定主题
```

工作流存了一份在 `notes/moss-decor-workflow.json`（8 步、1024×1024、负向词禁文字与人）。
依赖：ComfyUI 在 8188 运行，且 `extra_model_paths.yaml` 指向共享模型目录。

提示词写法：一段风格描述 + `seamless background texture for a chat app, subtle and low contrast,
soft gradients, no characters, no text, plenty of calm empty space`。
**明确写 no characters**，否则模型一定会塞人进去。
"""
t = t.rstrip() + "\n" + addition
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("docs ok")
