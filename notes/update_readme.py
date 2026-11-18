import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\README.md")
t = io.open(p, encoding="utf-8").read()

# 1) 功能表补一行：用量计费
t = t.replace(
    "| 生图 | 无 | BYOK 云端生图 |",
    "| 生图 | 无 | BYOK 云端生图 |\n| 用量计费 | — | 输入框下方实时显示 token、缓存命中、金额、上下文占用 |",
)

extra = """
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
"""
if "## 用量与计费" not in t:
    t = t.replace("## 上游\n", extra + "\n## 上游\n", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("README updated")
