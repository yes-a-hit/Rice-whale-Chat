import io, pathlib

base = pathlib.Path(r"E:\flutter\open-deepseek\dist")

plain = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  html,body{margin:0;padding:0;background:#333}
  iframe{width:390px;height:844px;border:0;display:block;background:#fff}
</style></head>
<body><iframe src="/"></iframe></body></html>
"""
io.open(base / "_device.html", "w", encoding="utf-8", newline="\n").write(plain)

keyed = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  html,body{margin:0;padding:0;background:#333}
  iframe{width:390px;height:844px;border:0;display:block;background:#fff}
</style></head>
<body>
<script>
  try {
    localStorage.setItem('ods:onboarded', 'true');
    localStorage.setItem('ods:ui-mode', 'plus');
    localStorage.setItem('ods:api-key', 'sk-dummy-preview');
    localStorage.setItem('ods:font-scale', '1');
  } catch (e) {}
</script>
<iframe src="/"></iframe></body></html>
"""
io.open(base / "_device-keyed.html", "w", encoding="utf-8", newline="\n").write(keyed)
print("frames rewritten")
