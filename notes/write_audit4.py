import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 18:10）

### 移除前端对模型输出的拦截（本轮）

官方 demo 在收到 `stop_reason: 'refusal'`（服务端安全拒答）时会**主动把已经生成的思考和正文丢掉**，
只剩一句固定话术——这就是「跟 deepseek 网页版一样拦截输出，而别的前端不会」的成因。
逐处拆掉：

| 文件 | 原行为 | 现在 |
|---|---|---|
| `src/services/chat/reply.ts` `settleReply` | refusal 时 `flatMap` 丢弃所有 thinking/text 块 | 改为 `map`，只给未结束的 thinking 补 `endedAt`，内容一律保留 |
| `src/services/chat/reply.ts` `canContinueReply` | `stopReason === 'refusal'` 直接 return false | 去掉该判断，拒答轮也能续写 |
| `src/services/chat/reply.ts` `isUsableReply` | `stopReason !== 'refusal'` 才进上下文 | 去掉该判断，拒答轮正常回传模型 |
| `src/services/chat/describe.ts` `describeReply` | refusal 时返回 `replyRefused` 固定话术 | 删掉整个分支，有正文就正常展示 |
| `src/components/messages/AssistantMessage.tsx` | `refused` 控制正文/思考区/搜索摘要/朗读/重新生成 | 全部去掉，正文与思考区照常渲染 |
| `src/services/api/parseEvent.ts` `message_delta` | stop_reason 不在白名单就丢掉整条事件（连 usage） | 只校验 delta 是对象，stop_reason 不再白名单 |

`toArchive.ts` 里 refusal → `CONTENT_FILTER` 的映射保留：只影响导出到官方格式时的状态字段，不隐藏内容。

### Lite 模式 UI 过大（本轮）

- 根因：`src/app/skins.ts` 用 `root.style.zoom = fontScale`（Lite 默认 1.15）放大整体界面，
  而 `src/app/App.module.css` 的 `.frame` 高度是 `var(--app-viewport-height)`（物理像素），
  被 zoom 再乘 1.15 → 底部输入框与免责声明被顶出屏幕。
- 修法：`applyAppearance()` 同时写 `--ods-zoom`，`.frame` 的高度与 top 改为
  `calc(var(--app-viewport-height, 100dvh) / var(--ods-zoom, 1))`；Lite 默认倍率 1.15 → 1.08，
  旧值 1.15 在 `initialFontScale()` 里自动收敛。
- Lite 首次进入若没手动设过 `thinking`，默认打开深度思考。

### 前端其它限制（现状，未改）

- `src/services/attachments.ts`：单文件 `MAX_SIZE_MB = 64`、单条消息 `MAX_USER_DATA_SIZE_MB = 32`、`MAX_COUNT = 50`、并发 `MAX_CONCURRENT = 3`。
- 输入框没有长度上限；附件类型走 `uploadExts.ts` 白名单（837 项）。
- 属内存/带宽保护，不是内容拦截。

### 验证

`pnpm type` 通过；`pnpm build` 通过；390×844 iframe 截图确认 zoom 1.15 与 1.08 下底部输入框完整可见、
设置三页不裁切。产物 `android/app/build/outputs/apk/release/app-release.apk`（6.7MB，v1.0.0-alpha.1，正式签名）。

### 仍未完成

- Kokoro-82M ONNX 推理与中文 G2P（`engines/kokoro.ts` 仍抛 `LOCAL_TTS_NOT_INSTALLED`）
- 原生 NPU 插件（ONNX Runtime Mobile QNN EP）
- 真机实测

## 构建

- 调试：`pnpm android:apk` → `app/build/outputs/apk/debug/app-debug.apk`
- 正式：`pnpm android:release` → `app/build/outputs/apk/release/app-release.apk`
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status)
print("audit ok")
