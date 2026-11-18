import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 18:34）

### 本轮七条（全部落地）

1. **系统提示词优先于角色卡**：`resolveSystemPrompt()` 改为「填了系统提示词就只用它」，系统提示词为空时才退回角色卡，两者都空才用官方默认。避免两套设定打架。
2. **包名**：`com.opendeepseek.chat` → `com.ricewhale.chat`（`capacitor.config.json`、`android/app/build.gradle` 的 namespace/applicationId、`MainActivity.java` 移到 `com/ricewhale/chat/`、`strings.xml` 的 app_name / package_name / custom_url_scheme）。`aapt2 dump badging` 确认 `package: name='com.ricewhale.chat' application-label:'Rice Whale Chat'`。
3. **极简模式保留深度思考**：`initialThinking` 在未经手动设置时对 lite 返回 true；联网搜索默认关；引导页文案改成明说这两点。
4. **改名**：`odsModeLite` = 极简模式（en: Minimal），README 表格同步。
5. **TTS 不再假装能用**：`engines/kokoro.ts` 注释写清 WebNN 拿不到 NPU、WebGPU 可能起不来；`readAloud.ts` 在配置为 kokoro 时直接回落 system 引擎并抛 `LOCAL_TTS_FALLBACK`，toast 提示「已改用系统朗读」。
6. **生图**：新增 `imageProvider: 'cloud' | 'local'`；Plus 模式两个触发口——输入框图片按钮、`/img`（含 `/draw`、`/pic`）指令直达弹窗并预填提示词。
7. **本地 NPU 生图通道**：`src/services/image/localPipeline.ts` 定义 `LocalImageStage`、`LocalImageOptions`（含 `onStage` 进度回调）、`LocalImageResult`，注释写明工作流 0.5B 提示词整理 → CLIP → SD-Turbo 1.5B → VAE → 落盘。`isLocalImageAvailable()` 检查 `globalThis.RiceWhaleBridge.localImage`，未接入时 `generateLocalImage()` 抛 `LOCAL_IMAGE_NOT_INSTALLED`。

### 实验性玩法（新分组）

设置从 4 个 tab 变 5 个：通用 / 扩展 / 用量 / **实验** / 数据。实验页收纳本地模型相关的一切：
算力设备检测、朗读引擎（含 kokoro）、**进阶 TTS**、本地生图通道、模型下载源、本地模型管理。

- 进阶 TTS 实现 `src/services/speech/contextVoice.ts`：`matchVoiceProfile(text, baseRate)` 按问句/感叹/代码/列表/平叙给你 `{mood, rate, pitch}`；`stripUnreadable()` 把代码块换成「这里有一段代码，先跳过」、删表格行与 URL。`system.ts` 的 `speakOne` 改为接收 tuning。
- 移动端 5 个 tab 收到 `min-width: 62px`、`font-size: 12.5px`，390px 宽全部放下（截图 `notes/lab-tab3.png`）。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 通过。产物 `android/app/build/outputs/apk/release/app-release.apk`（6.55MB，`com.ricewhale.chat`，v1.0.0-alpha.1）。

### 注意

- 改包名后是**新应用**，手机上原来那个 Open DeepSeek 不会自动升级，要手动卸载。
- 签名仍是同一个 jks，但包名不同，Android 视为两个应用。

### 仍未完成

- 本地 NPU 生图与本地 TTS 都只有接口，需要原生插件（ONNX Runtime Mobile + QNN EP）
- 真机实测

## 构建

- 调试：`pnpm android:apk` → `app/build/outputs/apk/debug/app-debug.apk`
- 正式：`pnpm android:release` → `app/build/outputs/apk/release/app-release.apk`
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status)
print("audit ok")
