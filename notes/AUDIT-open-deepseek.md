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

## 状态（2026-11-18 18:52）

### 图片全部转 WEBP

`notes/to_webp.py`（质量 82、method 6，RGBA 保 alpha）：

```
hungry.png   77 KB -> hungry.webp   51 KB
logo-128.png 12 KB -> logo-128.webp  3 KB
tech-mascot  510 KB -> 90 KB
wait.png     57 KB -> wait.webp     49 KB
welcome.png  88 KB -> welcome.webp  60 KB
maid-mascot  新     -> 57 KB
```

`dist/media` 总计 856 KB → 312 KB。组件引用全部改成 `.webp`（`Welcome` / `Sider` / `Onboarding` / `AssistantMessage`）。

### 主题体系

`src/app/themes/{types,registry}.ts` + `themes.css`，取代原 `skins.ts` 的 5 套配色（旧 id 自动回落 `plain`）。

- 七个内置：`plain` 最简 / `ink` 国风 / `maid` 经典女仆 / `tech` 科技 / `sumi` 水墨 / `moon` 月兔 / `gyu` 奶牛。
- 装饰走 `--ods-decor` 变量，由 `App.module.css` 的 `.frame` 拼到 `background-image` —— 不插 DOM、不挡点击。
- 自动匹配 `matchTheme()`：先比 `models` 再比 `hosts`，子串匹配，不写正则。当前只拿得到 `apiBaseUrl`，所以用 host 判断：`moonshot` → 月兔，`bigmodel`/`zhipu` → 奶牛。
- 设置项 `themeAuto`（默认关）；`selectTheme()` 里手动选择优先。
- 素材：`maid-mascot.webp` 由 `logo.png` 去白底生成；`tech-mascot.webp` 由 `tech-plus.jpg` 裁上半身 + 阈值抠深色背景生成。`moon`/`gyu` 暂无立绘，回落到默认图。
- 文档：`docs/themes.md`（配色变量清单、四步新增法、匹配规则、稳定性契约）。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 通过。截图：`notes/theme-tech.png`、`theme-maid.png`、`theme-sumi.png`。
产物 `android/app/build/outputs/apk/release/app-release.apk`（`com.ricewhale.chat`，v1.0.0-alpha.1）。

### 仍未完成

- 月兔、奶牛两套主题缺立绘（水兔女郎 / 萝莉牛娘），素材槽已留
- 本地 NPU 生图与本地 TTS 只有接口，需要原生插件
- 真机实测

## 构建

- 调试：`pnpm android:apk`
- 正式：`pnpm android:release`
