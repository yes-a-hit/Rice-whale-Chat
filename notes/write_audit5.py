import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 18:12）

### 梗图去白底（本轮）

`notes/strip_white.py` 从 `figure/*.jpg` 重新生成，可重复执行：

1. 亮度 ≥226 且饱和度 ≤26 的像素标记为「白」；
2. 用 `scipy.ndimage.binary_propagation` 从四边做连通扩散 —— **只把与画布边缘连通的白变透明**，
   人物白衣服、白眼白、对话气泡内部的白底全部保留；
3. alpha 做 sigma=0.8 的高斯软化后再阈值化，边缘不生硬；
4. 半透明像素按 alpha 反乘颜色（`(C - (1-a)*255)/a`）去掉白底光晕；
5. `MinFilter(3)` 收 1px，去掉残留浅灰线；
6. `quantize(colors=256, FASTOCTREE)` 压体积：welcome 487→89KB、no-key 441→57KB。

产物 `figure/out/welcome.png`（760×845，透明 61%）、`figure/out/no-key.png`（800×740，透明 57%）。
`Welcome.module.css` 的 `.mascotImage` 去掉 `border-radius`（透明图不再需要遮罩），改 `background: none`。
预览图（棋盘格）输出到 `notes/preview-*.jpg`，不再混进 `figure/out` 被 copy 进 APK。

### 移除前端拦截（上一轮）

`reply.ts` 的 `settleReply` / `canContinueReply` / `isUsableReply`、`describe.ts` 的 refusal 分支、
`AssistantMessage.tsx` 的 `refused` 门控、`parseEvent.ts` 的 stop_reason 白名单——全部拆掉，
`stop_reason: 'refusal'` 只当普通结束处理，正文与思考照常展示。

### Lite 模式 UI 过大（上一轮）

`skins.ts` 写 `--ods-zoom`，`.frame` 高度改 `calc(var(--app-viewport-height) / var(--ods-zoom))`；
Lite 默认倍率 1.15 → 1.08，旧值自动收敛。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 全通过。截图 `notes/alpha-pv-nokey.png`、
`notes/alpha-pv-keyed.png` 确认透明底融入页面、无白框。
产物 `android/app/build/outputs/apk/release/app-release.apk`（6.47MB，v1.0.0-alpha.1）。

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
