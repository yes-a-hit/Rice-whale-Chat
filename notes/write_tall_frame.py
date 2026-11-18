import io
import pathlib

base = pathlib.Path(r"E:\flutter\open-deepseek\dist")

html = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  html,body{margin:0;padding:0;background:#333}
  iframe{width:390px;height:1800px;border:0;display:block;background:#fff}
</style></head>
<body>
<script>
  try {
    localStorage.setItem('ods:onboarded', 'true');
    localStorage.setItem('ods:ui-mode', 'plus');
    localStorage.setItem('ods:api-key', 'sk-dummy-preview');
  } catch (e) {}
</script>
<iframe src="/#settings=ext"></iframe></body></html>
"""
io.open(base / "_tall-ext.html", "w", encoding="utf-8", newline="\n").write(html)
print("tall frame ok")
