# PLAN — Open-DeepSeek Chat

目标设备：**手机是主场**，其次是家里老登（五十多岁，初代网民，想学 AI）。因此一切「本地推理」必须跑在浏览器里，不能有 Python sidecar。

## 双模式

| | **Lite（老登模式）** | **Plus（重度模式）** |
|---|---|---|
| 界面 | 大字号、少按钮、单列、默认自动朗读 | 原版全功能 + 扩展面板 |
| 系统提示词 | 无（用官方默认一句话） | 可编辑（会话级覆盖 > 全局） |
| 角色卡 | 无 | 导入 chara card v2（PNG/JSON） |
| 皮肤 | 跟随系统深浅 | 内置 4 套 + 自定义主色 |
| TTS | 系统语音（零配置、离线、手机自带） | 三引擎可选：系统 / 本地 Kokoro（WebGPU/WASM）/ 官方云 TTS |
| ASR | 系统听写优先，回落本地 whisper | 本地 whisper-base（transformers.js）或官方 ASR |
| 生图 | 无 | BYOK 云端（OpenAI 兼容 / 硅基流动 / 即梦） |
| 群聊 | 无 | 无（明确不做） |

## 技术路线（浏览器内 NPU/算力）

- **统一后端抽象**：`src/services/speech/engines/` 下 `system` / `kokoro` / `cloud` 三个实现，统一输出 `MediaStream|AudioBuffer` 或直连 `speechSynthesis`。
- **NPU 通道**：`device: 'npu' | 'gpu' | 'cpu' | 'auto'`。WebNN 可用（`navigator.ml`）→ NPU；否则 WebGPU → GPU；否则 WASM → CPU。配置项保留 NPU 标识，不假装硬件存在。
- **模型下载**：`src/services/models/downloader.ts`，源可切 `hf-mirror.com`（默认）/ `huggingface.co` / `kaggle` 直链；进度条 + `CacheStorage` 缓存，二次加载零下载；支持手动「导入本地模型文件」给没网场景。
- **TTS 模型**：Kokoro-82M ONNX（q8，约 90MB）+ `phonemizer` wasm。中文走 zh voice。
- **ASR 模型**：`whisper-base` / `whisper-small`（transformers.js / onnxruntime-web）。
- **生图**：BYOK HTTP —— `POST {baseUrl}/images/generations`（OpenAI 兼容）+ 可配置模型名；不内置模型。

## 工单

### 阶段 A — 骨架（本次要做完）
1. 品牌隔离：包名、标题、`localStorage` 前缀 `ods:`、IndexedDB `open-deepseek`（含版本号 +1 迁移路径）。
2. **API 地址运行时化**：`API_ORIGIN` 构建期常量 → `apiBaseUrl` 设置项（默认 `https://api.deepseek.com`），客户端所有 URL 改读设置。手机填自己的反代/中转。
3. `uiMode` 设置 + 首启引导（选 Lite / Plus）；设置新增第三个分组「扩展」。
4. 构建跑通：`pnpm type` + `pnpm build` + 手机可访问（`pnpm dev --host`）。

### 阶段 B — Plus
5. 系统提示词编辑（全局 + 会话覆盖），`store.ts:38` 常量改为读取设置。
6. 角色卡导入：PNG（tEXt `chara` base64）/ JSON（chara_card_v2）；解析为 `name/description/personality/scenario/first_mes/system_prompt`，拼进 system。
7. 皮肤：`html[data-skin]` + 覆盖 `--dsw-static-*` 语义变量，4 套预设 + 自定义主色（OKLCH 生成）。

### 阶段 C — 语音与模型
8. TTS 引擎抽象 + 系统 TTS（Lite 默认，手机零配置离线）。
9. Kokoro-82M 本地引擎（WebGPU→WASM 降级），设备选项含 NPU。
10. 模型下载器（hf-mirror / kaggle / 本地导入）+ 缓存管理页。
11. ASR 本地通道（whisper-base），Lite 下用系统听写优先。

### 阶段 D — 生图与收尾
12. BYOK 生图（OpenAI 兼容 images API），结果进会话附件流。
13. 文档：README 中文版（部署到手机怎么用、老登模式怎么教、模型下载、隐私说明）。
14. 构建产物 + 部署脚本（静态托管 / 局域网静态服务）。

## 不做
- 群聊、多角色编排、世界书（保持比 rikkahub 轻）。
- 任何服务端；不存用户 key 到远端。

## 验收
- 手机浏览器可打开、可填 API 地址与 key、能流式聊天、能朗读（系统 TTS）。
- Lite 模式：首屏 3 个按钮以内，字号 ≥17px，朗读一键开。
- Plus 模式：改系统提示词后行为立即变化；导入 chara card v2 PNG 后首条消息按卡片人设回复。
- 模型下载：切 hf-mirror 能装完，断网后仍可本地 TTS。
