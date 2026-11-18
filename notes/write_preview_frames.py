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
    %(storage)s
  } catch (e) {}
</script>
<iframe src="/#preview"></iframe></body></html>
"""

nokey = """localStorage.removeItem('ods:api-key');
    localStorage.setItem('ods:onboarded', 'true');"""
keyed = """localStorage.setItem('ods:onboarded', 'true');
    localStorage.setItem('ods:ui-mode', 'plus');
    localStorage.setItem('ods:api-key', 'sk-dummy-preview');"""

for name, storage in (("pv-nokey", nokey), ("pv-keyed", keyed)):
    io.open(base / f"_{name}.html", "w", encoding="utf-8", newline="\n").write(
        tmpl % {"storage": storage}
    )
print("preview frames written")
