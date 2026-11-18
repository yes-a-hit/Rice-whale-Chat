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

## 状态（2026-11-18 18:24）

### 用量与计费（本轮）

- `src/services/billing.ts`（新）：`DEFAULT_PRICE = { cacheHit: 0.2, input: 2, output: 3, search: 0.01 }`（元/百万 token、元/次），
  `CONTEXT_LIMIT = 131_072`，`summarizeUsage()` 逐条累加 assistant 消息的 `usage` 与 `elapsedMs`。
- 耗时：`AssistantMessage` 加 `startedAt` / `elapsedMs`，`settleReply` 收尾时算差值，供 tok/s 使用。
- 底部状态条 `SessionStatsBar`（仅 Plus）：轮数 · 段数 · tok/s | token 总量 · 缓存命中率 | 金额 | 上下文占比。
- 设置新增「用量」tab：四色堆叠条（绿 cache hit / 红 input / 蓝 output / 橙 search）+ 明细 + 速率 + 上下文。
- 移动端四个 tab 收紧到 `min-width: 86px`，390px 宽正好放下。

### 生成参数（参考 chat-demo-unrestricted）

- `safety_check` 从硬编码改为可选：`sendSafetyCheck` 默认关（= 请求里不带该字段，服务端按最低档）。
- `temperature` / `top_p` / `max_tokens` 直调，`null` 表示不发送，设置里留空即恢复服务端默认。
- UI 在「设置 → 扩展 → 生成参数」。
- 与上游差异：上游 anti-retraction 那个开关我们直接做成默认行为（拦截整条链路已拆），不需要开关。

### 品牌与仓库

- 项目名 `rice-whale-chat`，Android 应用名 `Rice Whale Chat`（appId 仍 `com.opendeepseek.chat`，改包名会让已装的应用变成孤儿）。
- `origin` 指向 `https://github.com/yes-a-hit/Rice-whale-Chat`，上游保留为 `upstream`。
- 已推三个 commit：工程脚手架 / 应用实现 / 文档与素材，最新 `af3661b`。
- 三张梗图均为透明底 256 色 PNG：`welcome.png`（有 Key）、`hungry.png`（无 Key，「主人，奴家饿了」）、`wait.png`（余额不足提示里的小图）。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 全通过。
截图：`notes/hungry-key.png`（无 Key 欢迎页）、`notes/gen-ext.png`（生成参数）、`notes/usage-tab4.png`（用量 tab）。
产物 `android/app/build/outputs/apk/release/app-release.apk`（6.55MB，v1.0.0-alpha.1）。

### 仍未完成

- 计费的四色条只有空态截图，带数据的形态要等真机聊几轮再看
- Kokoro-82M ONNX 推理与中文 G2P（`engines/kokoro.ts` 仍抛 `LOCAL_TTS_NOT_INSTALLED`）
- 原生 NPU 插件（ONNX Runtime Mobile QNN EP）
- 真机实测

## 构建

- 调试：`pnpm android:apk` → `app/build/outputs/apk/debug/app-debug.apk`
- 正式：`pnpm android:release` → `app/build/outputs/apk/release/app-release.apk`
