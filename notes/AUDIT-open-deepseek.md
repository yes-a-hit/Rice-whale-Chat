# AUDIT — Open-DeepSeek Chat（基于 deepseek-ai/chat-demo）

日期：2026-11-17

## 目标
以官方静态前端 chat-demo（MIT）为基座，做一个自有发行版，双模式：
- **Lite / 老登模式**：原版功能全保留（流式、思考、搜索、附件、Markdown/KaTeX/Mermaid、分支、历史导入导出），额外接**本地算力 TTS**（NPU 优先，回落 GPU/CPU），模型走 **kaggle / hf-mirror 镜像**下载。
- **Plus 模式**：开放**系统提示词编辑**、**角色卡导入**（chara card v2 / JSON）、**换皮肤**、**本地/BYOK 生图**；单聊、轻量，不设群聊。

## 基座现状（已核对源码）
- 技术栈：TypeScript + React 18 + zustand 4 + rspack 2，纯静态无后端，`pnpm dev` 监听 8090。
- 目录：`src/app`（布局/主题）、`src/components/*`、`src/services/{api,chat,speech,markdown}`。
- 请求层 `src/services/api/client.ts`：Anthropic 兼容 `POST {API_ORIGIN}/anthropic/v1/messages`（SSE），`API_ORIGIN` 是**构建期常量**（`__API_ORIGIN__`，rspack DefinePlugin），默认 `https://api.deepseek.com`。
- 请求体 `CreateMessageRequest`（`src/services/api/types.ts:175`）**已含 `system: string` 字段**，客户端直接发送。
- 系统提示词是单行常量：`src/services/chat/store.ts:38` `const SYSTEM_PROMPT = '该助手为DeepSeek，由深度求索公司创造。'`，在 `store.ts:1003` 注入 → **plus 模式改这里即可，无需改协议**。
- 语音：`src/services/api/speech.ts` 走服务端 `/v1/tools/{asr,tts}`；播放端 `src/services/speech/readAloud.ts` 用 `AudioContext(24000Hz)` 边收边播 16-bit PCM 裸流。→ **本地 TTS 只要产出同格式 PCM 流即可无缝替换**。
- 设置：`src/services/settings.ts` zustand + localStorage（前缀 `chat-demo:*`）；UI 在 `src/components/settings/SettingsDialog.tsx`，两个分组 general/data（`sections` 数组 :48）。
- 存储：IndexedDB `chat-demo` v11，`Session` 类型 `{id,title,createdAt,updatedAt,messages,rootMessageId}`（`src/services/chat/types.ts:108`）；会话列表只读 summary。
- 主题：`src/app/theme.css` 206 个 CSS 变量（`--dsw-static-*` 语义色 + `--ds-*` 组件色），`body.dark`/`body.light`；`src/app/theme.ts` 有 `applyTheme`。→ **换皮肤 = `html[data-skin]` + 覆盖语义变量**。

## 本机环境（决定 NPU 方案）
- CPU：Intel i9-14900HX（**14 代 HX，无 Intel NPU**）；GPU：RTX 4070 Laptop（CUDA）+ Intel UHD。
- Python 3.12.8；ComfyUI 存在（`E:\Comfy-Desktop`）。
- 结论：本机"NPU"路径实际由 **OpenVINO/ONNX Runtime 设备选择**兜底：`npu → gpu → cpu` 自动降级；接口层保留 `device` 选项，符合"NPU 优先"意图。

## 约束
- 保持静态前端可双击运行（file:// 兼容尽量不掉）；本地服务只作为可选增强，连不上时自动回落服务端 TTS。
- 不引入重框架；plus 模式不新增会话模型字段以外的存储迁移（尽量零 DB 迁移）。
- 品牌与 localStorage/IndexedDB 前缀需与官方隔离（避免与线上 demo 数据串）。

## 未知项
- TTS 引擎选型（Kokoro-82M 轻 / CosyVoice2 中文自然）→ 待主人定。
- ASR 是否也本地化（faster-whisper）→ 待定。
- 生图后端：ComfyUI API（现有）还是自带 OpenVINO SD 管线 → 待定。

## 状态（2026-11-18 19:34）

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

**踩坑**：ComfyUI 默认只读自己的 `models/`，Comfy Desktop 的模型在 `E:\Comfy-Desktop\ComfyUI-Shared\models`。
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

- 调试：`pnpm android:apk`
- 正式：`pnpm android:release`
