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

## 状态（2026-11-18 20:45）

### 主题：立绘归属、欢迎语、夜间适配（m02581 / m02587）

**「换主题没用」的真因**：三处叠加 —— ① plain 与 ink 的主色都是青蓝，色相几乎一样；
② 装饰图的白色遮罩 0.84 把纹理压到看不见；③ 立绘七套里五套共用同一张。
所以换了主题视觉上确实没变化。

修法：

- **配色拉开**：plain 保持官方紫蓝（不设变量），ink 青绿 `#2f7d84`，maid 深藏蓝 `#3b4f8a`，
  tech 亮青 `#0093c4`，sumi 墨灰 `#4a4a48`，moon 紫 `#8a6fd6`，gyu 蓝灰 `#4a6f8f`。
- **遮罩下调**到 0.78–0.90，纹理可见。
- **每主题专属立绘**：用 moss 出 5 张白底立绘（`notes/run_mascot.py`，832×1216，10 步），
  再走 `notes/make_theme_mascots.py` 抠白 → `figure/out/<id>-mascot.webp`（57–93 KB）。
  - ink 汉服鲸鱼女仆 / plain 现代白卫衣 / sumi 黑色和服 / moon 月兔 / gyu 奶牛娘
  - 旧的 `welcome.webp`（汉服 + 烧在图里的气泡）退役删除，`hungry.webp` 保留共用
- **欢迎语改 DOM 气泡**：`Welcome.tsx` 里 `<div className={styles.bubble}>{t('odsWelcomeBubble')}</div>`，
  CSS 定位在图左上（`top: 10%`，`max-width: 44%`），带指向角色的小三角。
  i18n key 默认「欢迎回来，\n想从哪里开始」，换语言/措辞不用重出图。
- **夜间适配**：原来遮罩是写死的白色，深色模式下整屏发白。改成
  - `:root { --ods-veil-1/2: 白 }`、`body[data-ds-dark-theme='dark'] { --ods-veil-1/2: 近黑 }`
  - 主题只声明 `--ods-image: url(...)`，遮罩由 `.frame` 拼：`linear-gradient(var(--ods-veil-1), var(--ods-veil-2)), var(--ods-image, none)`
  - 关键教训：CSS 变量在**声明它的元素**上求值。`--ods-decor` 若写在 `html` 上，
    `var(--ods-veil)` 就按 html 的值算，body 上的夜间覆盖不参与。拆成两层后各自在自己的层求值才对。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 通过。APK 47.92MB。
浅色截图：`notes/t-ink.png`、`t-plain.png`、`t-moon.png`、`t-gyu.png`、`t-sumi.png`；
夜间截图：`notes/v-ink-dark.png`、`td-gyu.png`、`td-moon.png`、`td-sumi.png`。
`dist/media` 合计 630 KB（10 个 webp）。

### 仍未完成

- NPU 上真跑模型（模型转换 + 中文 G2P）
- 上下文压缩
- 真机实测（NPU 检测、主题切换、夜间模式）

## 构建

- 调试：`pnpm android:apk`
- 正式：`pnpm android:release`
