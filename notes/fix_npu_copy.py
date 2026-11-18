import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- NPU 两格文案区分清楚 ----------
pairs_zh = [
    ("odsNpuNoWebnn", "浏览器这层没有 WebNN。真 NPU 只能走上面那格「NPU 原生桥」，Web 侧最多用 WebGPU"),
    ("odsNpuNoDevice", "浏览器有 WebNN 但只开放 CPU/GPU，没有 npu 设备类型。真 NPU 看上面那格"),
    ("odsNpuOk", "浏览器可以直接用 NPU"),
    ("odsComputeDevice", "浏览器算力（Web）"),
    ("odsComputeDeviceHint", "点「检测」查看 Web 侧拿到的 WebNN / WebGPU / WASM 能力；真 NPU 看上一格的「NPU 原生桥」"),
]
pairs_en = [
    ("odsNpuNoWebnn", "No WebNN in this WebView. Real NPU comes from the native bridge above"),
    ("odsNpuNoDevice", "WebNN only exposes CPU/GPU here. Check the native bridge above for real NPU"),
    ("odsNpuOk", "Browser-level NPU available"),
    ("odsComputeDevice", "Browser compute (Web)"),
    ("odsComputeDeviceHint", "Tap Detect to see WebNN / WebGPU / WASM; real NPU is the native bridge above"),
]

for path, pairs in (("src/i18n/zh.ts", pairs_zh), ("src/i18n/en.ts", pairs_en)):
    p = root / path
    t = io.open(p, encoding="utf-8").read()
    for key, value in pairs:
        lines = t.split("\n")
        for index, line in enumerate(lines):
            if line.strip().startswith(f"{key}:"):
                lines[index] = f"  {key}: '{value}',"
                break
        t = "\n".join(lines)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("i18n ok", path)
