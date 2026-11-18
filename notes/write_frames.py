import io, pathlib

tmpl = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  html,body{margin:0;padding:0;background:#333}
  iframe{width:390px;height:844px;border:0;display:block;background:#fff}
</style></head>
<body><iframe src="/#settings=%(section)s"></iframe></body></html>
"""

base = pathlib.Path(r"E:\flutter\open-deepseek\dist")
for section in ("ext", "data", "general"):
    io.open(base / f"_device-{section}.html", "w", encoding="utf-8", newline="\n").write(
        tmpl % {"section": section}
    )
print("frames written")
