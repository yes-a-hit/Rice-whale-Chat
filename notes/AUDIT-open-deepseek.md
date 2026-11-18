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

## 状态（2026-11-18 18:12）

### 梗图去白底（本轮）

`notes/strip_white.py` 从 `figure/*.jpg` 重新生成，可重复执行：

1. 亮度 ≥226 且饱和度 ≤26 的像素标记为「白」；
2. 用 `scipy.ndimage.binary_propagation` 从四边做连通扩散 —— **只把与画布边缘连通的白变透明**，
   人物白衣服、白眼白、对话气泡内部的白底全部保留；
3. alpha 做 sigma=0.8 的高斯软化后再阈值化，边缘不生硬；
4. 半透明像素按 alpha 反乘颜色（`(C - (1-a)*255)/a`）去掉白底光晕；
5. `MinFilter(3)` 收 1px，去掉残留浅灰线；
6. `quantize(colors=256, FASTOCTREE)` 压体积：welcome 487→89KB、no-key 441→57KB。

产物 `figure/out/welcome.png`（760×845，透明 61%）、`figure/out/no-key.png`（800×740，透明 57%）。
`Welcome.module.css` 的 `.mascotImage` 去掉 `border-radius`（透明图不再需要遮罩），改 `background: none`。
预览图（棋盘格）输出到 `notes/preview-*.jpg`，不再混进 `figure/out` 被 copy 进 APK。

### 移除前端拦截（上一轮）

`reply.ts` 的 `settleReply` / `canContinueReply` / `isUsableReply`、`describe.ts` 的 refusal 分支、
`AssistantMessage.tsx` 的 `refused` 门控、`parseEvent.ts` 的 stop_reason 白名单——全部拆掉，
`stop_reason: 'refusal'` 只当普通结束处理，正文与思考照常展示。

### Lite 模式 UI 过大（上一轮）

`skins.ts` 写 `--ods-zoom`，`.frame` 高度改 `calc(var(--app-viewport-height) / var(--ods-zoom))`；
Lite 默认倍率 1.15 → 1.08，旧值自动收敛。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 全通过。截图 `notes/alpha-pv-nokey.png`、
`notes/alpha-pv-keyed.png` 确认透明底融入页面、无白框。
产物 `android/app/build/outputs/apk/release/app-release.apk`（6.47MB，v1.0.0-alpha.1）。

### 仍未完成

- Kokoro-82M ONNX 推理与中文 G2P（`engines/kokoro.ts` 仍抛 `LOCAL_TTS_NOT_INSTALLED`）
- 原生 NPU 插件（ONNX Runtime Mobile QNN EP）
- 真机实测

## 构建

- 调试：`pnpm android:apk` → `app/build/outputs/apk/debug/app-debug.apk`
- 正式：`pnpm android:release` → `app/build/outputs/apk/release/app-release.apk`
