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

## 状态（2026-11-18 19:26）

### NPU 原生桥（路线 C）

用户选择真上 QNN。已完成骨架，桥能通，模型接入未做。

- `android/app/build.gradle`：
  - `ndk { abiFilters 'arm64-v8a' }`
  - `implementation "com.microsoft.onnxruntime:onnxruntime-android-qnn:1.20.0"`
  - `packagingOptions.jniLibs.excludes` 裁掉 `libQnnHtpPrepare.so`（42MB）、Gpu/Cpu/Dsp、V68/V69 Skel
- `android/app/src/main/java/com/ricewhale/chat/NpuPlugin.java`（新）：`@CapacitorPlugin(name="Npu")`，
  `available()` 返回 ort 是否在包内、QNN HTP 库能否 `System.loadLibrary`、ABI、`Build.SOC_MODEL`、SDK；
  `providers()` 反射调 `OrtEnvironment.getAvailableProviders()`。
- `MainActivity.java` 在 `super.onCreate` 前 `registerPlugin(NpuPlugin.class)`。
- `src/services/npu.ts`（新）：`readNpuStatus()` / `readNpuProviders()`，浏览器环境返回 `unavailable` 不抛错。
- `LabSettings.tsx` 加 `NpuBridgeCell`（实验页第一格），点检测显示 `ORT ✓ · QNN ✓ · SoC · ABI` 与 EP 列表。

**包体积**：未裁剪时 115MB，裁完 47.6MB。剩下的：libonnxruntime 16MB + V75Skel 12MB + V73Skel 7MB + QnnHtp 1MB。
V73/V75 都留，因为 7s Gen 4 的 HTP 版本没确认；实测后可按 SoC 再删一个。

**未做**：模型转换（ONNX + QDQ int8）、中文 G2P、`loadModel/run` 接口、真机调优。
文档：`docs/npu.md`。

### 检测文案修正

`src/services/device.ts` 加 `nativeBridge` 字段与 `explainCompute()`；`LabSettings` 的算力检测
现在会说明「浏览器没有 WebNN / 有 WebNN 但只开放 CPU-GPU」，不再是干巴巴的 ✗。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 通过。APK 47.6MB。
`zipfile` 确认只打包 8 个 .so。截图 `notes/npu-cell2.png`。

### 仍未完成

- NPU 上真跑模型（模型转换 + G2P）
- 上下文压缩
- 月兔/奶牛专属立绘
- 真机实测

## 构建

- 调试：`pnpm android:apk`
- 正式：`pnpm android:release`
