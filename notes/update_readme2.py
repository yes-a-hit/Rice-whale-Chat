import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\README.md")
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    "| | **Lite（老登模式）** | **Plus（重度模式）** |",
    "| | **极简模式** | **Plus（重度模式）** |",
)
t = t.replace("| 界面 | 字号放大、隐藏深度思考/搜索开关 | 完整功能 |",
              "| 界面 | 字号放大、按钮精简（深度思考保留，联网搜索默认关） | 完整功能 |")
t = t.replace("## 给长辈用（Lite）", "## 给长辈用（极简模式）")

# 实验性玩法一节，插在「用量与计费」之前
lab = """## 实验性玩法

设置 → **实验**。这一组默认全关，开了也不保证跑得起来——本地推理在 Android WebView 里
拿不到 Hexagon NPU，只能落到 WebGPU 或 WASM，部分机型直接起不来。单独放一页，出问题不影响日常聊天。

| 项 | 现状 |
|---|---|
| 本地算力设备 | 可以点「检测」看 WebNN / WebGPU / WASM SIMD 支持情况与线程数 |
| 朗读引擎 | 本地模型 TTS（Kokoro）尚未接通运行时，选中会自动回落系统朗读并提示一句 |
| **进阶 TTS** | 按上下文配音：问句放慢、感叹句加快、列表多停顿，代码与表格换成口播话术、跳过链接 |
| 本地生图通道 | 接口已留好，行为为空。工作流：`0.5B 改写提示词 → CLIP → SD-Turbo 1.5B → VAE → 落盘 + 预览` |
| 模型下载源 | hf-mirror / huggingface / kaggle 直连 |
| 本地模型 | Kokoro-82M、Whisper-base，下载后存设备上可离线使用 |

生图有两个触发方式，都在 Plus 模式：

- 输入框右侧的图片按钮
- 输入 `/img 一只戴草帽的鲸鱼娘`（也认 `/draw`、`/pic`），回车直接弹生图面板并预填提示词

## 用量与计费"""
t = t.replace("## 用量与计费", lab, 1)

# 包名说明
t = t.replace(
    "产物：`android/app/build/outputs/apk/debug/app-debug.apk`（约 6 MB）",
    "产物：`android/app/build/outputs/apk/debug/app-debug.apk`（约 6 MB）\n\n包名 `com.ricewhale.chat`，应用名 `Rice Whale Chat`。",
)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("README ok")
