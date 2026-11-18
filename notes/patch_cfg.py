import io, json, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\capacitor.config.json")
cfg = json.loads(io.open(p, encoding="utf-8").read())
# 允许 http 的局域网中转地址（用户在设置里填 192.168.x.x 时用），同时保留 https 默认
cfg["android"]["allowMixedContent"] = True
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(cfg, ensure_ascii=False, indent=2))
print(json.dumps(cfg, ensure_ascii=False))
