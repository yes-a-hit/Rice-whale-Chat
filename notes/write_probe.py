import io, pathlib

html = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>body{font:28px/1.6 monospace;margin:0;padding:20px}div{margin:6px 0}</style></head>
<body>
<div id="w"></div><div id="h"></div><div id="dpr"></div><div id="mob"></div>
<script>
document.getElementById('w').textContent = 'innerWidth=' + window.innerWidth;
document.getElementById('h').textContent = 'innerHeight=' + window.innerHeight;
document.getElementById('dpr').textContent = 'dpr=' + window.devicePixelRatio;
document.getElementById('mob').textContent = 'isMobile=' + window.matchMedia('not all and (min-width: 768px)').matches;
document.body.style.background = '#ffd';
</script>
</body></html>
"""
io.open(pathlib.Path(r"E:\flutter\open-deepseek\dist\_probe.html"), "w", encoding="utf-8", newline="\n").write(html)
print("probe written")
