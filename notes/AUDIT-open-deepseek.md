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

## 状态（2026-11-18 21:05）

### 五条反馈：1-3 已修，4-5 出计划

**1. 版本号没更新** → 1.0.0-alpha.1 bump 到 1.1.0-alpha.1，versionCode 1010001，
apt2 dump badging 已确认。

**2. 主题一片白** → 根治：配色从 CSS 挪进 TS（	hemes/registry.ts 的 palette 与 image），
套用时 skins.ts 的 pplyAppearance() 用 
oot.style.setProperty **写成行内变量**。
行内样式优先级最高，不再依赖 html[data-theme] 选择器能否匹配。
	hemes.css 只剩遮罩色（--ods-veil-1/2）与说明。
截图验证：
otes/iv-ink.png、iv-tech.png、iv-sumi.png。

**3. NPU 检测冲突** → 两格本来就是两层东西：上面「NPU 原生桥」是 Capacitor 原生插件（ORT/QNN），
下面「浏览器算力（Web）」是 Web API。改文案把这件事说透：
odsNpuNoWebnn = 「浏览器这层没有 WebNN。真 NPU 只能走上面那格『NPU 原生桥』，Web 侧最多用 WebGPU」，
odsComputeDevice 改名「浏览器算力（Web）」，hint 里直接指向上一格。

**4. 生图 BYOK / 本地模型 / LoRA** → 计划见 
otes/PLAN-local-ai.md。
现状：云端四个字段是散的、本地没有任何模型入口、没有 LoRA 概念。
计划：新增生图设置分组（通道切换 + 云端五项 + 本地推荐模型 + LoRA 多选 + 导入），
先做纯 UI 与存储（1–5 步），推理后端等 NPU/WebGPU 就绪。

**5. 本地跑千问** → 计划同上。选型建议 ONNX Runtime GenAI（与现有 ORT 同栈），
模型 Qwen2.5-1.5B-int4（约 1GB）/ 3B-int4（约 2GB）。
不做 tool calling / 联网 / 深度思考——小模型会胡说。

### 验证

pnpm type / pnpm build / ssembleRelease 通过。APK 47.9MB，1.1.0-alpha.1。

### 仍未完成

- 生图与本地 LLM（计划已出）
- NPU 上真跑模型（模型转换 + 中文 G2P）
- 上下文压缩
- 真机实测

## 构建

- 调试：pnpm android:apk
- 正式：pnpm android:release
