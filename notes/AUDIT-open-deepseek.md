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

## 状态（2026-11-18 21:20）

### 三条小活已落地

1. **自动折叠思考**：设置项 collapseThinking（默认关），开启后流式期间展开、回答开始/结束自动收起；
   ReplyArea.tsx 用 useEffect 监听 streaming。UI 在「扩展」页默认开关区。
2. **计费实时**：DEFAULT_PRICE 改成官方口径（缓存命中 0.5 / 输入 2 / 输出 8，元每百万 token）；
   SessionStatsBar 把 status=pending 的回复按「字符数 / 1.6」估 output token 并计入费用，
   生成过程中数字会动。
3. **模型选择**：ChatModel 改为 deepseek-v4.1-flash / deepseek-v4-pro；
   settings 加 model；store.ts 的常量 MODEL 换成 currentModel() 读设置；
   ChatInput 加 ModelPicker：Lite 是「快速 / 专家」两个胶囊，Plus 是一个下拉。

**踩坑（重要）**：initialModel() 定义在 useSettings = create() 之后，
production 构建（压缩后）报 Cannot access 'ep' before initialization——
const 箭头函数在模块顶层初始化前被调用就是 TDZ。dev 模式不报是因为没压缩。
教训：所有 initialXxx() 必须定义在 create() 之前。

**踩坑（样式）**：模型选择器一开始放在 .toggles 内部，被 .collapsedToggles .toggleLabel{display:none}
的折叠逻辑吃掉文字。挪到 toggles 外面才稳定显示。

### 新增五条（m02997）已出计划


otes/PLAN-plus.md：可编辑/删除回复（4h）、per-conversation agent 与 preset（8h，依赖角色卡）、
角色卡独立可调与绑定背景（10h）、归档与分类（5h）、知识库工作流清洗→提炼→入库→RAG（~21h）。
建议顺序：1 → 4 → 3 → 2 → 5。

### 验证

pnpm type / pnpm build / ssembleRelease 通过。APK 47.82MB，1.1.0-alpha.1。
截图 
otes/n-lite.png（快速/专家胶囊）、
otes/n-plus.png（下拉）。

## 构建

- 调试：\pnpm android:apk\n- 正式：\pnpm android:release\n