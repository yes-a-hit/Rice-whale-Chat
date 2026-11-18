import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, sep, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 00:10）

- [x] 基座克隆 + 审计（本文件）
- [x] 阶段 A 骨架：品牌隔离（包名 `com.opendeepseek.chat`、localStorage 前缀 `ods:`）、**API 地址运行时化**（`getApiOrigin()` + 设置项 `apiBaseUrl`）、`uiMode` 双模式、首启选模式引导、设置新增「扩展」分组
- [x] 阶段 B Plus：系统提示词编辑（`resolveSystemPrompt()` 注入 `store.ts` 的 system 字段）、角色卡导入（JSON / PNG tEXt，chara card v2/v3）、5 套皮肤（`html[data-skin]` 覆盖 `--dsw-static-blue-*`）、字号缩放（`html.style.zoom`）
- [x] 阶段 C 部分：朗读引擎抽象（`services/speech/engines/{system,kokoro,cloud}.ts`，统一 `TtsEngine` 接口）、系统语音（离线、按句切分）、云端 TTS（沿用原 PCM 流）、Lite 模式回复完自动朗读；模型清单 + 下载器（hf-mirror / HuggingFace / Kaggle / 手动，CacheStorage 缓存 + 进度 + 删除）
- [x] 阶段 D 部分：BYOK 生图（OpenAI 兼容 `/images/generations`，Plus 模式输入区按钮）
- [x] Capacitor Android 工程 + APK 出包（`android/app/build/outputs/apk/debug/app-debug.apk`，约 6MB）
- [ ] 阶段 C 未完：Kokoro-82M 的 ONNX 推理与音素转换未接（`engines/kokoro.ts` 目前抛 `LOCAL_TTS_NOT_INSTALLED`）；Whisper 本地 ASR 同理
- [ ] 原生 NPU 插件（ONNX Runtime Mobile QNN EP）未做

## 构建要点

- JDK 17 + Capacitor 7（默认 Java 21）冲突：`android/build.gradle` 里用 `subprojects { afterEvaluate { compileOptions 17 } }` 降到 17，已生效
- Windows 下 `NODE_ENV=...` 前缀无效：构建脚本改为 `rspack build --mode production`，`rspack.config.ts` 里用 `process.argv.includes('--mode=production')` 判定
- Capacitor CLI 7 加载 `capacitor.config.ts` 在 TypeScript 7 下崩溃（`reading 'CommonJS'`）：改用 `capacitor.config.json`
- 模拟器会拖死本机，已确认不在本机跑模拟器验证

## 下一步

1. 真机装 APK，验证：首启引导 → 填 key → 流式回复 → 系统 TTS 朗读 → 切 Plus → 改提示词 → 导入角色卡
2. 接 Kokoro 推理（`onnxruntime-web` + espeak-ng wasm；中文 G2P 用 misaki 或 pinyin 表）
3. 若要真 NPU：Capacitor 插件包 ONNX Runtime Mobile，`computeDevice` 的 `npu` 分支桥到 QNN EP
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status)
print("audit updated")
