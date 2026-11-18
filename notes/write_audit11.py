import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\notes\AUDIT-open-deepseek.md")
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 19:26）

### NPU 原生桥（路线 C）

用户选择真上 QNN。已完成骨架，桥能通，模型接入未做。

- `android/app/build.gradle`：
  - `ndk { abiFilters 'arm64-v8a' }`
  - `implementation "com.microsoft.onnxruntime:onnxruntime-android-qnn:1.20.0"`
  - `packagingOptions.jniLibs.excludes` 裁掉 `libQnnHtpPrepare.so`（42MB）、Gpu/Cpu/Dsp、V68/V69 Skel
- `android/app/src/main/java/com/ricewhale/chat/NpuPlugin.java`（新）：`@CapacitorPlugin(name="Npu")`，
  `available()` 返回 ort 是否在包内、QNN HTP 库能否 `System.loadLibrary`、ABI、`Build.SOC_MODEL`、SDK；
  `providers()` 反射调 `OrtEnvironment.getAvailableProviders()`。
- `MainActivity.java` 在 `super.onCreate` 前 `registerPlugin(NpuPlugin.class)`。
- `src/services/npu.ts`（新）：`readNpuStatus()` / `readNpuProviders()`，浏览器环境返回 `unavailable` 不抛错。
- `LabSettings.tsx` 加 `NpuBridgeCell`（实验页第一格），点检测显示 `ORT ✓ · QNN ✓ · SoC · ABI` 与 EP 列表。

**包体积**：未裁剪时 115MB，裁完 47.6MB。剩下的：libonnxruntime 16MB + V75Skel 12MB + V73Skel 7MB + QnnHtp 1MB。
V73/V75 都留，因为 7s Gen 4 的 HTP 版本没确认；实测后可按 SoC 再删一个。

**未做**：模型转换（ONNX + QDQ int8）、中文 G2P、`loadModel/run` 接口、真机调优。
文档：`docs/npu.md`。

### 检测文案修正

`src/services/device.ts` 加 `nativeBridge` 字段与 `explainCompute()`；`LabSettings` 的算力检测
现在会说明「浏览器没有 WebNN / 有 WebNN 但只开放 CPU-GPU」，不再是干巴巴的 ✗。

### 验证

`pnpm type` / `pnpm build` / `assembleRelease` 通过。APK 47.6MB。
`zipfile` 确认只打包 8 个 .so。截图 `notes/npu-cell2.png`。

### 仍未完成

- NPU 上真跑模型（模型转换 + G2P）
- 上下文压缩
- 月兔/奶牛专属立绘
- 真机实测

## 构建
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status + "\n- 调试：`pnpm android:apk`\n- 正式：`pnpm android:release`\n")
print("audit ok")
