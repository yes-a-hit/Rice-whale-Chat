# Open DeepSeek

基于 [`deepseek-ai/chat-demo`](https://github.com/deepseek-ai/chat-demo)（MIT）改造的手机端聊天应用，用 Capacitor 打成 APK。

两个模式共用同一份密钥与聊天记录，随时在「设置 → 扩展」里切换。

| | **极简模式** | **Plus（重度模式）** |
|---|---|---|
| 界面 | 字号放大、按钮精简（深度思考保留，联网搜索默认关） | 完整功能 |
| 朗读 | 回复完成后自动朗读（可在设置里换引擎） | 手动点小喇叭 |
| 系统提示词 | 官方默认 | 可编辑 / 导入角色卡 |
| 皮肤 | 跟随系统深浅 | 5 套主色可选 |
| 生图 | 无 | BYOK 云端生图 |
| 用量计费 | — | 输入框下方实时显示 token、缓存命中、金额、上下文占用 |

## 安装

```powershell
cd E:\flutter\open-deepseek
pnpm install
pnpm android:apk
```

产物：`android/app/build/outputs/apk/debug/app-debug.apk`（约 6 MB）

包名 `com.ricewhale.chat`，应用名 `Rice Whale Chat`。

装到手机：

```powershell
adb install -r android\app\build\outputs\apk\debug\app-debug.apk
```

或者把 APK 拷进手机点击安装（首次需允许「安装未知来源应用」）。

## 首次使用

1. 打开应用 → 选 **Lite** 或 **Plus**
2. 左下角头像 → 设置 → **数据管理** → 填 DeepSeek API Key
3. 手机没连外网/用中转时，到「扩展 → 聊天服务地址」改成你自己的地址（默认 `https://api.deepseek.com`）

## 给长辈用（极简模式）

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


## 主题

设置 → 扩展 → 主题。七个内置：

| 主题 | 风格 |
|---|---|
| 最简（原版） | 官方蓝，无装饰 |
| 国风 | 青蓝水墨，鲸鱼娘立绘 |
| 经典女仆 | 深蓝白蕾丝斜纹，女仆装 |
| 科技 | 青蓝荧光网格，机能风 |
| 水墨 | 墨色留白，大面积晕染 |
| 月兔（Kimi） | 米白淡紫，月晕 |
| 奶牛（GLM） | 黑白斑点 |

**跟随接口自动换主题**：打开后，服务地址含 `moonshot` 自动切月兔，含 `bigmodel` 自动切奶牛。
手动选择优先于自动。

主题是可扩展的：加一段 CSS 变量 + 一条注册项就行，格式与社区约定见 [docs/themes.md](docs/themes.md)。

## 实验性玩法

设置 → **实验**。这一组默认全关，开了也不保证跑得起来——本地推理在 Android WebView 里
拿不到 Hexagon NPU，只能落到 WebGPU 或 WASM，部分机型直接起不来。单独放一页，出问题不影响日常聊天。

| 项 | 现状 |
|---|---|
| 本地算力设备 | 可以点「检测」看 WebNN / WebGPU / WASM SIMD 支持情况与线程数 |
| 朗读引擎 | 本地模型 TTS（Kokoro）尚未接通运行时，选中会自动回落系统朗读并提示一句 |
| **进阶 TTS** | 按上下文配音：问句放慢、感叹句加快、列表多停顿，代码与表格换成口播话术、跳过链接 |
| 本地生图通道 | 接口已留好，行为为空。工作流：`0.5B 改写提示词 → CLIP → SD-Turbo 1.5B → VAE → 落盘 + 预览` |
| 模型下载源 | hf-mirror / huggingface / kaggle 直连 |
| 本地模型 | Kokoro-82M、Whisper-base，下载后存设备上可离线使用 |

生图有两个触发方式，都在 Plus 模式：

- 输入框右侧的图片按钮
- 输入 `/img 一只戴草帽的鲸鱼娘`（也认 `/draw`、`/pic`），回车直接弹生图面板并预填提示词

## 用量与计费

**Plus 模式**下，输入框下方有一条实时状态：

```
12 轮 · 86 段 · 152 tok/s      1.2M tok · 缓存 93%      ¥0.41      7%
```

依次是：对话轮数、内容段数、生成速率、token 总量、缓存命中率、估算花费、上下文占用。

设置里另有 **用量** 页，用四色堆叠条看构成：

| 颜色 | 含义 |
|---|---|
| 🟩 绿 | 缓存命中（`cache_read_input_tokens`） |
| 🟥 红 | 输入、未命中缓存（`input_tokens`） |
| 🟦 蓝 | 输出（`output_tokens`） |
| 🟧 橙 | 联网检索（按次计费） |

单价按 DeepSeek 官方价写在 `src/services/billing.ts` 的 `DEFAULT_PRICE`，单位元 / 百万 token：

```ts
cacheHit: 0.2,   // 命中缓存
input: 2,        // 未命中
output: 3,       // 输出
search: 0.01,    // 每次联网检索
```

要改就改这一个常量。上下文窗口按 128K（`CONTEXT_LIMIT`）算占比，取最近一轮的输入加输出。

## 目录结构

```
src/
  app/            应用外壳、主题皮肤、布局
  components/     UI：聊天、消息、设置、计费、生图、引导
  services/
    api/          流式请求、事件解析、余额、语音接口
    chat/         会话仓库、消息视图、归档导入导出
    speech/       TTS 引擎（system / cloud / kokoro）
    models/       本地模型清单与下载（hf-mirror / kaggle）
    billing.ts    用量与计费
    settings.ts   全部设置项（localStorage，前缀 ods:）
    characterCard.ts  角色卡（PNG tEXt / JSON）
figure/           品牌素材与透明底梗图（构建时拷进 dist/media）
android/          Capacitor 生成的 Android 工程
notes/            审计、计划、脚本、验证截图
```

## 上游

- 上游英文说明：[README.upstream.md](README.upstream.md)
- 上游中文说明：[README.upstream.zh-CN.md](README.upstream.zh-CN.md)

## 协议

MIT，与上游 chat-demo 一致。

## 版本与签名

版本号写在 `package.json` 的 `version`，格式固定为 **`1.x.y-tag.z`**：

| 段 | 含义 |
|---|---|
| `1` | 主版本，协议/数据格式大改才动 |
| `x` | 次版本，加功能 |
| `y` | 修订号，修 bug |
| `tag` | `alpha` / `beta` / `rc`，正式版不带 tag |
| `z` | 同一 tag 内的递增序号 |

`android/app/build.gradle` 读这个版本号，同时算出 `versionName` 与 `versionCode`：

```
versionCode = major*1000000 + minor*10000 + patch*100 + tag序号
1.0.0-alpha.1  →  versionCode 1000001
```

日常用脚本改，不用手改：

```bash
pnpm version:bump            # 看当前版本与 versionCode
pnpm version:bump tag        # 1.0.0-alpha.1 -> 1.0.0-alpha.2
pnpm version:bump patch      # -> 1.0.1-alpha.1
pnpm version:bump minor      # -> 1.1.0-alpha.1
pnpm version:bump stable     # -> 1.1.0（正式版）
```

签名材料在 `android/` 下（**不进版本库**）：

- `android/app/open-deepseek-release.jks`：RSA 2048，有效期 10000 天
- `android/keystore.properties`：别名与密码

只要 `keystore.properties` 存在，`assembleRelease` 就自动用正式签名；文件不存在时回退 debug 签名，不影响本地调试。**这两个文件丢了就没法覆盖升级已安装的版本**，务必自己留一份备份。

```bash
pnpm android:release         # 出签名包
# 产物：android/app/build/outputs/apk/release/app-release.apk
```
