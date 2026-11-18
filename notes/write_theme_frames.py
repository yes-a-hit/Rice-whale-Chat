import io
import pathlib

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
    localStorage.setItem('ods:api-key', 'sk-dummy-preview');
    localStorage.setItem('ods:skin', '%(theme)s');
  } catch (e) {}
</script>
<iframe src="/#preview"></iframe></body></html>
"""

for theme in ("plain", "ink", "maid", "tech", "sumi"):
    io.open(base / f"_theme-{theme}.html", "w", encoding="utf-8", newline="\n").write(
        tmpl % {"theme": theme}
    )
print("theme frames ok")
