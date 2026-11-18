# 本地 AI 功能计划（生图 / 本地 LLM）

> 状态：计划，未开工。主人 m02732 提的第 4、5 条。

## 4. 生图：BYOK 配置菜单 + 本地模型管理

### 现状问题

`ExtSettings.tsx` 里只有四个散字段（Base URL / Key / 模型 / 开关），
`LabSettings.tsx` 里有「本地生图通道」下拉，但：

- 选了 BYOK 没有对应的完整配置（缺尺寸默认值、超时、代理）
- 选了本地没有任何模型下载/导入入口
- 没有 LoRA 概念

### 目标结构

新增「生图」设置分组（或并入实验页，取决于入口多少）：

```
生图
├── 通道        [云端 BYOK] [本地 ONNX]
├── 云端（BYOK 时显示）
│   ├── 服务地址   https://api.openai.com/v1
│   ├── API Key    ••••
│   ├── 模型       dall-e-3 / flux-schnell / ...
│   ├── 默认尺寸   1024×1024
│   └── [测试连接]
└── 本地（本地时显示）
    ├── 推荐模型（可下载，带体积与显存要求）
    │   ├── SD-Turbo 1.5B int8      ~1.1 GB   ✓ 已适配
    │   ├── SDXL-Turbo int8         ~2.6 GB   未验证
    │   └── 文本编码器 CLIP ViT-L   ~250 MB   必装
    ├── LoRA（可选，多选生效）
    │   ├── 导入 .safetensors → 存在应用私有目录
    │   └── 权重强度滑块 0–1
    └── [导入本地模型]  ← file picker，接受 .onnx / .safetensors
```

### 实现拆解

| # | 工作 | 文件 | 估时 |
|---|---|---|---|
| 1 | 设置数据结构：`imageProvider` 已存在，补 `imageSize`、`imageTimeout`、`imageLoras: {path, scale}[]` | `src/services/settings.ts` | 0.5h |
| 2 | 云端配置 UI（含「测试连接」调一次 `/models`） | `src/components/settings/ImageSettings.tsx`（新） | 1.5h |
| 3 | 本地模型注册表：`MODELS` 加 `kind: 'tts' | 'asr' | 'image' | 'clip' | 'lora'` | `src/services/models/registry.ts` | 1h |
| 4 | 模型下载/导入 UI（复用现有 `ModelsSection`，按 kind 分组） | `ModelsSection.tsx` | 1.5h |
| 5 | LoRA 导入：`<input type=file accept=".safetensors">` → 写 OPFS → 记录元数据 | `src/services/models/lora.ts`（新） | 1.5h |
| 6 | 本地生图管线接 LoRA 权重 | `src/services/image/localPipeline.ts` | 依赖原生桥 |

**前置**：本地生图要真跑起来，得先有能跑 SD 的原生/WebGPU 推理后端。
目前 `localPipeline.ts` 只有接口（抛 `LOCAL_IMAGE_NOT_INSTALLED`）。
建议顺序：先做 1–5（纯 UI + 存储，能立刻交付），第 6 步等 NPU/WebGPU 后端。

## 5. 本地跑小语言模型（千问 2B / 4B）

### 技术选型

| 方案 | 优点 | 缺点 |
|---|---|---|
| **ONNX Runtime GenAI Android** | 有官方 AAR，和现有 ORT 同栈；支持 XNNPACK/NNAPI | 模型要转成 ORT 格式，工具链折腾 |
| llama.cpp JNI | 生态最全，GGUF 模型满地都是 | 要自己编 NDK + 写 JNI，包体 +20MB |
| onnxruntime-web + WebGPU | 不碰原生，改 JS 就行 | 7s Gen 4 上 1.5B int4 大概 3–8 tok/s，发热明显 |

建议 **ORT GenAI**：已经在用 ORT，`onnxruntime-genai-android` 能复用 QNN/CPU EP。

### 模型

- `Qwen2.5-1.5B-Instruct-int4`（约 1.0 GB）—— 手机上最现实的选择
- `Qwen2.5-3B-Instruct-int4`（约 2.0 GB）—— 16G RAM 能扛，速度慢一半

主人说「会很傻」是对的：1.5B int4 的中文能力大约相当于 GPT-3.5 的六成，
写代码、长推理基本不能看，适合「离线问答 + 简单改写」。

### 实现拆解

| # | 工作 | 估时 |
|---|---|---|
| 1 | `onnxruntime-genai-android` AAR 接入 + 包体评估（预计 +25MB） | 1h |
| 2 | `LocalLlmPlugin.java`：`loadModel(path)` / `generate(prompt, maxTokens, onToken)` | 3h |
| 3 | JS 侧 `src/services/llm/local.ts`：包装成流式回调 | 2h |
| 4 | 模型下载：HF 上 `microsoft/Phi-3.5-mini`、`Qwen/Qwen2.5-1.5B-Instruct` 的 ORT 版本 | 2h |
| 5 | 接口层：`apiBaseUrl` 加一个虚拟值 `local://qwen`，命中时走本地引擎 | 2h |
| 6 | 设置项：本地模型选择 + 上下文长度 + 温度（复用现有参数 UI） | 1h |

**不做**：tool calling、联网搜索、深度思考（小模型做不了，会胡说）。

### 风险

- 16G RAM 里加载 1GB 模型 + KV cache，后台被杀概率高
- 生成时 CPU 满载发热，手机可能降频
- 首次加载 5–15 秒，要有进度提示
