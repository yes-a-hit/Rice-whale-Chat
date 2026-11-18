import io, pathlib

content = """# Open DeepSeek

基于 [`deepseek-ai/chat-demo`](https://github.com/deepseek-ai/chat-demo)（MIT）改造的手机端聊天应用，用 Capacitor 打成 APK。

两个模式共用同一份密钥与聊天记录，随时在「设置 → 扩展」里切换。

| | **Lite（老登模式）** | **Plus（重度模式）** |
|---|---|---|
| 界面 | 字号放大、隐藏深度思考/搜索开关 | 完整功能 |
| 朗读 | 回复完成后自动朗读（可在设置里换引擎） | 手动点小喇叭 |
| 系统提示词 | 官方默认 | 可编辑 / 导入角色卡 |
| 皮肤 | 跟随系统深浅 | 5 套主色可选 |
| 生图 | 无 | BYOK 云端生图 |

## 安装

```powershell
cd E:\\flutter\\open-deepseek
pnpm install
pnpm android:apk
```

产物：`android/app/build/outputs/apk/debug/app-debug.apk`（约 6 MB）

装到手机：

```powershell
adb install -r android\\app\\build\\outputs\\apk\\debug\\app-debug.apk
```

或者把 APK 拷进手机点击安装（首次需允许「安装未知来源应用」）。

## 首次使用

1. 打开应用 → 选 **Lite** 或 **Plus**
2. 左下角头像 → 设置 → **数据管理** → 填 DeepSeek API Key
3. 手机没连外网/用中转时，到「扩展 → 聊天服务地址」改成你自己的地址（默认 `https://api.deepseek.com`）

## 给长辈用（Lite）

- 选 Lite 后字号自动放大 15%，输入区的「深度思考 / 联网搜索」开关隐藏
- 每回答完一条会自动朗读；不想听就在回复下方点停止，或在「扩展 → 朗读引擎」换引擎
- 语音提问用输入框右侧的麦克风（走手机自带听写，不花 token）
- 聊天记录存在手机本地，不上传

## Plus 功能

- **系统提示词**：扩展 → 系统提示词，保存后对新回复立即生效
- **角色卡**：支持 chara card v2 的 JSON 或内嵌数据的 PNG（SillyTavern 导出的那种），导入后自动拼成系统提示词
- **皮肤**：DeepSeek 蓝 / 海蓝 / 樱粉 / 森林 / 石墨，只改主色阶
- **生图**：输入框的图片按钮，填 OpenAI 兼容的 `/images/generations` 服务（服务地址 + Key + 模型名）

## 本地模型

扩展 → 本地模型：

- **下载源**：`hf-mirror`（国内推荐）/ `HuggingFace` / `Kaggle` / 手动导入
- 下载的文件存在 CacheStorage，断网可用；删除即释放
- 目前清单：Kokoro-82M（TTS）、Whisper-base（ASR）

> 本地 TTS 的推理管线（ONNX Runtime Web + 音素转换）还没接上，当前朗读走「系统语音」或「云端 TTS」，两者都可用。模型下载与缓存已经能用。

## 开发

```powershell
pnpm dev          # 浏览器调试，8090 端口
pnpm type         # 类型检查
pnpm build        # 生产构建到 dist/
pnpm android:sync # 构建并同步进 Android 工程
pnpm android:apk  # 出 debug APK
```

## 目录

```
src/
  app/                  布局、主题、皮肤
  components/settings/  设置（通用 / 扩展 / 数据管理）
  components/onboarding 首次启动选模式
  components/image      生图弹窗
  services/
    api/                请求层（Anthropic 兼容 SSE）
    chat/               会话状态与 IndexedDB
    speech/             朗读引擎：system / kokoro / cloud
    models/             模型清单、下载与缓存
    image/              BYOK 生图
    characterCard.ts    角色卡解析（PNG tEXt / JSON）
    device.ts           WebNN / WebGPU / WASM 能力探测
android/                Capacitor 生成的原生工程
```

## 已知限制

- 手机 WebView 里 WebNN 拿不到 Hexagon NPU；真要吃 NPU 需要原生插件（ONNX Runtime Mobile QNN EP），接口层已按 `computeDevice: auto|npu|gpu|cpu` 预留
- 缝 Local Dream 需要 fork 它的 native 库或走它的 Intent 接口，与前端框架无关
- 生图依赖你填的服务，应用本身不代理任何流量

## 上游

- 上游英文说明：[README.upstream.md](README.upstream.md)
- 上游中文说明：[README.upstream.zh-CN.md](README.upstream.zh-CN.md)

## 协议

MIT，与上游 chat-demo 一致。
"""

p = pathlib.Path(r"E:\flutter\open-deepseek\README.md")
io.open(p, "w", encoding="utf-8", newline="\n").write(content)
print("README written", len(content))
