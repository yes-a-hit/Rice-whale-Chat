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

## 状态（2026-11-18 21:35）

### 主题：图标跟着换 + 素材归位（m03264 / m03279）

- **每套主题自己的 logo**：
otes/make_theme_logos.py 从各 <id>-mascot.webp 裁头部 → igure/out/<id>-logo.webp；
  
egistry.ts 每套主题 ssets.logo 指向自己的；Sider.tsx / Onboarding.tsx 从硬编码 /media/logo-128.webp
  改成 	hemeAsset(useSettings(selectTheme), 'logo')。换主题时侧栏和引导页的小头像一起换。
- **国风用回最初的 meme 图**：
otes/fix_ink_and_tech_logo.py 从 igure/welcome.jpg（汉服鲸鱼女仆，气泡在图里）
  裁切去白底 → ink-mascot.webp；Theme 加 uiltinBubble?: boolean，ink 设 true，
  Welcome.tsx 在这种情况下不再渲染 DOM 气泡，避免双气泡。
- **女仆立绘抠图修复**：
otes/fix_maid_mascot.py 用 (top >= 238) & ((top - low) <= 12) + 四边连通，
  只抠外部背景（36.9%），白围裙/白领子/白花边全部保住。
- **装饰底图不显示**：decor-*.webp 原本只放在 src/app/themes/assets/，而 skins.ts 拼的是 /media/ → 404。
  已复制到 igure/out/ 交给 CopyRspackPlugin，dist/media 现在六个 decor 齐全。奶牛斑块额外调淡（向白混 55%）。

### 模型方案（m03359）

settings.ts 新增 ProviderPreset { id, name, baseUrl, apiKey?, model }、presets、ctivePreset，
内置三套：DeepSeek 官方 / OpenAI / 自定义（OpenAI 兼容）。pplyPreset(id) 把方案的地址、模型、Key 写进当前生效设置；
savePreset / 
emovePreset 管列表。ChatModel 放宽为 string，第三方模型名不受限。
UI 在「扩展」页「模型方案」：点一行即切换，编辑可改名称/地址/模型/专用 Key。
Lite 的快速 / 专家仍绑 deepseek-v4.1-flash / deepseek-v4-pro。

### 验证

pnpm type / pnpm build / ssembleRelease 通过。APK 47.95MB。截图：
otes/tz-maid.png（女仆修好）、

otes/tl-ink.png（国风老图 + 单气泡）、
otes/preset-ext.png（模型方案）。

## 构建

- 调试：pnpm android:apk
- 正式：pnpm android:release
