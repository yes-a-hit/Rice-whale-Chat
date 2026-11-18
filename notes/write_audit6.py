import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 18:24）

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
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status)
print("audit ok")
