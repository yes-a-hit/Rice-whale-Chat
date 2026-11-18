import io
import pathlib
import re
import zipfile

root = pathlib.Path(r"E:\flutter\open-deepseek")
apk = root / "android/app/build/outputs/apk/release/app-release.apk"
dist_index = root / "dist/index.html"

html = io.open(dist_index, encoding="utf-8").read()
dist_js = re.findall(r"main\.[0-9a-f]+\.js", html)
print("dist js:", dist_js, "apk MB:", round(apk.stat().st_size / 1048576, 2))

with zipfile.ZipFile(apk) as z:
    inside = z.read("assets/public/index.html").decode("utf-8")
    print("apk  js:", re.findall(r"main\.[0-9a-f]+\.js", inside))
    name = "assets/public/static/js/" + dist_js[0]
    payload = z.read(name)
    for probe in ("供应商与模型", "odsProvidersHint", "供应商 + 模型"):
        print(f"  {probe}:", probe.encode() in payload)
    print("  media count:", len([n for n in z.namelist() if n.startswith("assets/public/media/")]))
