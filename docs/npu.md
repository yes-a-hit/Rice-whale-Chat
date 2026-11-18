# NPU 通道（Android / 骁龙 Hexagon）

## 为什么浏览器里检测不到

手机 SoC 有 NPU，但**浏览器这层没有通往它的门**：

| 层 | 情况 |
|---|---|
| Android WebView | 不支持 WebNN（Chromium 在 WebView 里关掉了） |
| Chrome for Android | 有 WebNN，但只暴露 `deviceType: 'cpu' \| 'gpu'`；`npu` 只在 ChromeOS / Windows Copilot+ 这类有 ML Service 的平台 |
| 原生代码 | QNN SDK / SNPE / NNAPI，唯一入口 |

所以 JS 能拿到的算力上限是 WebGPU（Adreno）。要真吃 Hexagon，必须走原生。

## 现在的架构

```
WebView (JS)
   │  Capacitor bridge
   ▼
NpuPlugin.java          android/app/src/main/java/com/ricewhale/chat/NpuPlugin.java
   │  ai.onnxruntime.*
   ▼
ONNX Runtime Mobile  +  QNN Execution Provider
   │
   ▼
Hexagon HTP (libQnnHtp.so + libQnnHtpV7xSkel.so)
```

JS 侧封装在 `src/services/npu.ts`：

```ts
import { readNpuStatus, readNpuProviders } from './services/npu'

const status = await readNpuStatus()
// { ort: true, qnnLibrary: true, soc: 'SM7635', abi: 'arm64-v8a', ... }
```

设置 → 实验 → **NPU 原生桥** → 检测，会显示 ORT / QNN 是否就绪、SoC 型号、ABI，
以及 ORT 编译进来的 Execution Provider 列表（应包含 `QNNExecutionProvider`）。

## 包体积

`com.microsoft.onnxruntime:onnxruntime-android-qnn` 把所有代 Hexagon 后端都打进来，未裁剪时 APK 115MB。

裁剪后 47.6MB，只剩：

| 库 | 大小 | 用途 |
|---|---|---|
| `libonnxruntime.so` | 16 MB | 推理运行时 |
| `libQnnHtpV75Skel.so` | 12 MB | Hexagon V75 后端 |
| `libQnnHtpV73Skel.so` | 7 MB | Hexagon V73 后端 |
| `libQnnHtp.so` | 1 MB | HTP 加载器 |
| `libQnnSystem.so` | <1 MB | QNN 系统接口 |

裁掉的（`android/app/build.gradle` 的 `packagingOptions.jniLibs.excludes`）：

- `libQnnHtpPrepare.so`（42 MB）—— 离线模型准备工具，运行时用不到
- `libQnnGpu.so` / `libQnnCpu.so` —— 我们只走 NPU
- `libQnnDsp.so` / `libQnnDspV66Skel.so` —— 老 DSP
- `libQnnHtpV68Skel.so` / `V69Skel.so` —— 更老的 SoC

ABI 只保留 `arm64-v8a`。

> **装到真机后如果 `qnnLibrary: false`**，说明这套 Skel 版本跟芯片对不上。
> 把 `V68/V69` 的 exclude 去掉再构建，或者查一下 `Build.SOC_MODEL` 对应的 HTP 版本。

## 还没做的部分

桥通了只是第一步，真跑起来还需要：

1. **模型转换**：目标模型 → ONNX（opset ≤ 20）→ QDQ 量化 int8，逐个算子验证 QNN 支持情况。
   Kokoro-82M 社区有 ONNX 版，但要过一遍 `onnxruntime_perf_test` 看有没有回落到 CPU 的算子。
2. **中文 G2P**：Kokoro 吃的是 phoneme 序列，需要 pinyin → phoneme 的转换表，
   或者在 NDK 里塞 espeak-ng。
3. **推理接口**：`NpuPlugin` 增加 `loadModel` / `run` 方法，JS 侧接 `LocalTtsEngine`。
4. **真机调优**：`htp_performance_mode`（burst / balanced / power_saver）、
   `enable_htp_fp16_precision`、图缓存（`htp_graph_finalization_optimization_mode`）。

## 验证方法

1. 装 APK（`com.ricewhale.chat`）
2. 设置 → 实验 → NPU 原生桥 → 检测
3. 期望看到 `ORT ✓ · QNN ✓ · SM7635 · arm64-v8a`，展开应有 `QNNExecutionProvider`

`QNN ✗` 多半是 Skel 版本不匹配，见上面那行。
`ORT ✗` 说明 AAR 没打进包，检查 `dependencies` 里的 `onnxruntime-android-qnn`。
