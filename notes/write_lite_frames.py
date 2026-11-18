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
    localStorage.setItem('ods:ui-mode', 'lite');
    localStorage.setItem('ods:api-key', 'sk-dummy-preview');
    localStorage.setItem('ods:font-scale', '1.08');
  } catch (e) {}
</script>
<iframe src="/#settings=%(section)s"></iframe></body></html>
"""

for section in ("general", "ext", "data"):
    io.open(base / f"_lite-{section}.html", "w", encoding="utf-8", newline="\n").write(
        tmpl % {"section": section}
    )
print("lite frames ok")
