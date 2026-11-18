import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

pairs_zh = [
    ("odsNpuNativeReady", "原生桥已就绪，可以走 QNN / NNAPI 真 NPU 推理"),
    (
        "odsNpuNoWebnn",
        "浏览器没有 WebNN：NPU 只能从原生代码调用，Web 侧最多用 WebGPU（Adreno）",
    ),
    (
        "odsNpuNoDevice",
        "有 WebNN 但浏览器只开放 CPU/GPU：Android 上 npu 设备类型不可用，真 NPU 要走原生插件",
    ),
    ("odsNpuOk", "浏览器直连 NPU 可用"),
]
pairs_en = [
    ("odsNpuNativeReady", "Native bridge present: QNN / NNAPI available"),
    ("odsNpuNoWebnn", "No WebNN in this WebView: NPU needs native code, Web can only use WebGPU"),
    ("odsNpuNoDevice", "WebNN exists but only CPU/GPU: true NPU needs a native plugin"),
    ("odsNpuOk", "Browser-level NPU available"),
]

for path, pairs in (("src/i18n/zh.ts", pairs_zh), ("src/i18n/en.ts", pairs_en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    if pairs[0][0] in t:
        continue
    tail = "} as const" if path.endswith("zh.ts") else "} satisfies Record<keyof typeof zh, string>"
    t = t.replace(tail, "".join(f"  {k}: '{v}',\n" for k, v in pairs) + tail, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("ok", path)
