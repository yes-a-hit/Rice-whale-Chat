import io, pathlib

html = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  html,body{margin:0;padding:0;background:#333}
  iframe{width:390px;height:844px;border:0;display:block;background:#fff}
</style></head>
<body><iframe src="/#settings"></iframe></body></html>
"""
io.open(pathlib.Path(r"E:\flutter\open-deepseek\dist\_device.html"), "w", encoding="utf-8", newline="\n").write(html)
print("device frame written")
