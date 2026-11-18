# AGENT-CARD — open-deepseek

**硬约束（来自 `E:\flutter\AGENTS.md`）**
- 不开 Android 模拟器调试（会拖死本机）；验证靠真机 adb 或浏览器 `pnpm dev`
- 改含中文的源文件用 Python `io.open(encoding='utf-8')`，不用 PowerShell 管道
- 内联多行 python 写成 `.py` 再跑

**项目**
- 根：`E:\flutter\open-deepseek`（chat-demo + Capacitor）
- 双模式：Lite（大字、自动朗读、只留深度思考）/ Plus（提示词、角色卡、皮肤、生图）
- 出包：`pnpm android:apk` → `android/app/build/outputs/apk/debug/app-debug.apk`

**关键坑**
- JDK 17 vs Capacitor 7（Java 21）：`android/build.gradle` 的 `subprojects{afterEvaluate{compileOptions 17}}` 兜底
- Windows 无 `NODE_ENV=` 前缀：`rspack build --mode production`
- `capacitor.config.ts` 在 TS7 下加载崩溃：用 `capacitor.config.json`
- PowerShell 改文件会毁 UTF-8 中文

**未完成**
- Kokoro ONNX 推理（`services/speech/engines/kokoro.ts` 抛 `LOCAL_TTS_NOT_INSTALLED`）
- 原生 NPU 插件（ONNX Runtime Mobile QNN EP）
