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

## 状态（2026-11-18 18:34）

### 本轮七条（全部落地）

1. **系统提示词优先于角色卡**：`resolveSystemPrompt()` 改为「填了系统提示词就只用它」，系统提示词为空时才退回角色卡，两者都空才用官方默认。避免两套设定打架。
2. **包名**：`com.opendeepseek.chat` → `com.ricewhale.chat`（`capacitor.config.json`、`android/app/build.gradle` 的 namespace/applicationId、`MainActivity.java` 移到 `com/ricewhale/chat/`、`strings.xml` 的 app_name / package_name / custom_url_scheme）。`aapt2 dump badging` 确认 `package: name='com.ricewhale.chat' application-label:'Rice Whale Chat'`。
3. **极简模式保留深度思考**：`initialThinking` 在未经手动设置时对 lite 返回 true；联网搜索默认关；引导页文案改成明说这两点。
4. **改名**：`odsModeLite` = 极简模式（en: Minimal），README 表格同步。
5. **TTS 不再假装能用**：`engines/kokoro.ts` 注释写清 WebNN 拿不到 NPU、WebGPU 可能起不来；`readAloud.ts` 在配置为 kokoro 时直接回落 system 引擎并抛 `LOCAL_TTS_FALLBACK`，toast 提示「已改用系统朗读」。
6. **生图**：新增 `imageProvider: 'cloud' | 'local'`；Plus 模式两个触发口——输入框图片按钮、`/img`（含 `/draw`、`/pic`）指令直达弹窗并预填提示词。
7. **本地 NPU 生图通道**：`src/services/image/localPipeline.ts` 定义 `LocalImageStage`、`LocalImageOptions`（含 `onStage` 进度回调）、`LocalImageResult`，注释写明工作流 0.5B 提示词整理 → CLIP → SD-Turbo 1.5B → VAE → 落盘。`isLocalImageAvailable()` 检查 `globalThis.RiceWhaleBridge.localImage`，未接入时 `generateLocalImage()` 抛 `LOCAL_IMAGE_NOT_INSTALLED`。

### 实验性玩法（新分组）

设置从 4 个 tab 变 5 个：通用 / 扩展 / 用量 / **实验** / 数据。实验页收纳本地模型相关的一切：
算力设备检测、朗读引擎（含 kokoro）、**进阶 TTS**、本地生图通道、模型下载源、本地模型管理。

- 进阶 TTS 实现 `src/services/speech/contextVoice.ts`：`matchVoiceProfile(text, baseRate)` 按问句/感叹/代码/列表/平叙给你 `{mood, rate, pitch}`；`stripUnreadable()` 把代码块换成「这里有一段代码，先跳过」、删表格行与 URL。`system.ts` 的 `speakOne` 改为接收 tuning。
- 移动端 5 个 tab 收到 `min-width: 62px`、`font-size: 12.5px`，390px 宽全部放下（截图 `notes/lab-tab3.png`）。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 通过。产物 `android/app/build/outputs/apk/release/app-release.apk`（6.55MB，`com.ricewhale.chat`，v1.0.0-alpha.1）。

### 注意

- 改包名后是**新应用**，手机上原来那个 Open DeepSeek 不会自动升级，要手动卸载。
- 签名仍是同一个 jks，但包名不同，Android 视为两个应用。

### 仍未完成

- 本地 NPU 生图与本地 TTS 都只有接口，需要原生插件（ONNX Runtime Mobile + QNN EP）
- 真机实测

## 构建

- 调试：`pnpm android:apk` → `app/build/outputs/apk/debug/app-debug.apk`
- 正式：`pnpm android:release` → `app/build/outputs/apk/release/app-release.apk`
