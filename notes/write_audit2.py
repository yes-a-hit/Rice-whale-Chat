import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 00:25）

### 手机实测反馈的第一轮修复（全部完成）

| # | 反馈 | 处理 |
|---|---|---|
| 1 | 不适配 UI | 设置弹窗移动端改为全宽底部面板（`width/max-width:100%`、`margin-right:0` 修掉右侧裁切）、`viewport-fit=cover`、`frame` 加安全区 padding、内容区可滚动、禁用横向滚动条 |
| 2 | 缺乏回设置通道 | `MobileHeader` 右侧常驻齿轮按钮（任何页面都能进设置）；首启引导完成后才检查 API Key，不再抢在引导页前面弹设置 |
| 3 | 删除位置信息 | `SettingsDialog` 的 `LocationSetting` 组件与其导入整体移除；`services/location.ts` 保留但不再引用 |
| 4 | 可配置语音 | 新增 `ttsRate`（0.5–2 倍速滑块）、`ttsSystemVoice`（列出手机已装中文语音）、云端音色选择；`engines/system.ts` 读这两项 |
| 5 | 提示词与角色卡分离 | 新增 `characterPrompt` / `characterName`；`resolveSystemPrompt()` 改为「全局提示词 + 角色卡」拼接，两者互不覆盖 |
| 6 | 本地数据库 | 数据管理新增「本地数据库」卡片：会话数 / 消息数 / 占用与配额（`navigator.storage.estimate`）、刷新、清理缓存（保留 `ods-models` 模型缓存） |
| 7 | 余额 | 数据管理顶部「账户余额」：`GET {origin}/user/balance`，显示各币种总余额与可用状态，可刷新 |

### 顺带修掉的真 bug

- **Lite 自动朗读从未生效**：之前那次 patch 只改了 App.tsx 的一半，`onReplyDone` 订阅缺失。现在补回：Lite 模式下回复完成即朗读，错误用 toast 说明。
- **慢加载死循环**：IndexedDB 打不开时永远转圈，3 秒后出现「重试」按钮（`location.reload()`）。
- Lite 模式首次切换默认打开深度思考（`setUiMode('lite')` 内联动）。

### 调试脚手架（保留，无害）

- `#settings` / `#settings=ext` / `#settings=data`：URL hash 直接打开设置对应分组。
- 本地验证不依赖模拟器：`pnpm build` → `python -m http.server 8091 --directory dist`，再用 iframe 390×844 页面套住应用截图（`notes/write_mode_frames.py` 生成 `dist/_device-*.html`）。

### 仍未完成

- Kokoro-82M ONNX 推理与中文 G2P（`engines/kokoro.ts` 仍抛 `LOCAL_TTS_NOT_INSTALLED`）
- 原生 NPU 插件（ONNX Runtime Mobile QNN EP）
- 真机实测（需主人安装 APK 后反馈）

## 构建

`pnpm android:apk` → `android/app/build/outputs/apk/debug/app-debug.apk`（约 6MB）

已知坑：JDK 17 vs Capacitor 7 的 Java 21（`android/build.gradle` 兜底）、`capacitor.config.json` 而非 `.ts`、Windows 无 `NODE_ENV=` 前缀。
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status)
print("audit updated")
