import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 00:30）

### 品牌资源（本轮）

素材统一放在 `figure/`，构建时由 `rspack.CopyRspackPlugin` 拷到 `dist/media/`：

| 素材 | 用途 | 处理 |
|---|---|---|
| `figure/logo.png`（512×512 女仆鲸鱼娘） | 应用图标 / 引导页 / 侧栏品牌 | `notes/make_icons.py` 生成 mipmap 各 dpi 的 `ic_launcher.png` / `ic_launcher_round.png`（圆形遮罩）/ `ic_launcher_foreground.png`（adaptive，内容占 66%），并重做 `drawable*/splash.png`；`figure/out/logo-128.png` 给界面用 |
| `figure/welcome.jpg` | 欢迎页 | 裁掉左右空白后缩到 760 宽、256 色量化 → `figure/out/welcome.png`（222KB） |
| `figure/no-key.jpg` | 没填 API Key 时的欢迎页 | 800 宽、256 色量化 → `figure/out/no-key.png`（167KB） |

界面接入：
- `src/components/session/Welcome.tsx`：按 `apiKey` 切换 `welcome.png` / `no-key.png`；无 Key 时图下方给出「还差一个 API Key → 去设置」按钮（`odsWelcomeAddKey`）。
- `src/components/settings/settingsDialogState.ts` 的 `ensureApiKey()` 改为只返回布尔值，**不再自动弹设置**——没 Key 时长辈看到的是图，不是一屏表单。
- `src/components/onboarding/Onboarding.tsx`：标题上方加 92px 圆角 logo。
- `src/components/sider/Sider.tsx`：侧栏品牌行改为 `logo + appName`。

### 手机实测反馈的第一轮修复（上一轮，全部完成）

| # | 反馈 | 处理 |
|---|---|---|
| 1 | 不适配 UI | 设置弹窗移动端全宽底部面板、修 `margin-right:-24px` 的右侧裁切、`viewport-fit=cover`、安全区 padding、标签栏可横滑 |
| 2 | 缺设置入口 | `MobileHeader` 右上角常驻齿轮 |
| 3 | 删位置信息 | `LocationSetting` 组件与导入整体移除 |
| 4 | 可配置语音 | `ttsRate` 滑块、`ttsSystemVoice` 下拉、云端音色选择 |
| 5 | 提示词与角色卡分离 | `systemPrompt` / `characterPrompt` 两个独立字段，`resolveSystemPrompt()` 拼接 |
| 6 | 本地数据库 | `DataSection`：会话数/消息数/占用配额、刷新、清理缓存 |
| 7 | 余额 | `GET {origin}/user/balance`，显示各币种余额 |

### 调试脚手架（保留，正常使用不受影响）

- `#settings` / `#settings=ext` / `#settings=data`：直接打开设置分组。
- `#preview`：跳过 IndexedDB 等待直接渲染欢迎页。
- 手机布局验证：`python -m http.server 8091 --directory dist` + 390×844 iframe（`notes/write_*.py` 生成 `dist/_device*.html`、`dist/_pv-*.html`）。

### 仍未完成

- Kokoro-82M ONNX 推理与中文 G2P（`engines/kokoro.ts` 仍抛 `LOCAL_TTS_NOT_INSTALLED`）
- 原生 NPU 插件（ONNX Runtime Mobile QNN EP）
- 真机实测

## 构建

`pnpm android:apk` → `android/app/build/outputs/apk/debug/app-debug.apk`（约 7.8MB）
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status)
print("audit updated")
