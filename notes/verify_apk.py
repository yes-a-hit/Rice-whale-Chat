import io
import pathlib
import re
import zipfile

root = pathlib.Path(r"E:\flutter\open-deepseek")
apk = root / "android/app/build/outputs/apk/release/app-release.apk"
dist_index = root / "dist/index.html"

print("APK mtime:", apk.stat().st_mtime, "size MB:", round(apk.stat().st_size / 1048576, 2))
html = io.open(dist_index, encoding="utf-8").read()
print("dist js:", re.findall(r"main\.[0-9a-f]+\.js", html))

with zipfile.ZipFile(apk) as z:
    names = [n for n in z.namelist() if n.endswith("assets/public/index.html")]
    print("apk index entries:", names)
    if names:
        inside = z.read(names[0]).decode("utf-8")
        print("apk js:", re.findall(r"main\.[0-9a-f]+\.js", inside))
        print("apk css:", re.findall(r"main\.[0-9a-f]+\.css", inside))
    # 检查最新文案是否在 js 里
    js_names = [n for n in z.namelist() if n.startswith("assets/public/static/js/main")]
    print("apk js files:", js_names[:3])
    for name in js_names[:1]:
        payload = z.read(name)
        for probe in ("供应商与模型", "odsProviders", "模型方案", "odsProviderModels"):
            print(f"  {probe}:", "供应商与模型".encode() in payload if probe == "供应商与模型" else probe.encode() in payload)
