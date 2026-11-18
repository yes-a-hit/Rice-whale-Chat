import io, pathlib

base = pathlib.Path(r"E:\flutter\open-deepseek\dist")

tmpl = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  html,body{margin:0;padding:0;background:#333}
  iframe{width:390px;height:844px;border:0;display:block;background:#fff}
</style></head>
<body>
<script>
  try {
    localStorage.setItem('ods:onboarded', 'true');
    localStorage.setItem('ods:ui-mode', '%(mode)s');
    localStorage.setItem('ods:api-key', 'sk-dummy-preview');
    localStorage.setItem('ods:font-scale', '%(scale)s');
  } catch (e) {}
</script>
<iframe src="/"></iframe></body></html>
"""

for name, mode, scale in (("lite", "lite", "1.15"), ("plus", "plus", "1")):
    io.open(base / f"_device-{name}.html", "w", encoding="utf-8", newline="\n").write(
        tmpl % {"mode": mode, "scale": scale}
    )
print("mode frames written")
