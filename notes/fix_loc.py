import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/components/settings/SettingsDialog.tsx"
lines = io.open(p, encoding="utf-8").read().split("\n")

# LocationSetting 从 213 行（1-based）开始，到 277 行前（LocaleSetting 的注释）结束
start = next(i for i, line in enumerate(lines) if line.startswith("const LocationSetting = () => {"))
# 往上吸收紧邻的注释块
up = start
while up > 0 and lines[up - 1].strip().startswith(("/*", "*", "//")) or (up > 0 and lines[up - 1].strip().endswith("*/")):
    up -= 1
    if lines[up].strip().startswith("/**"):
        break
# 往下到下一个组件的注释/定义之前
end = start + 1
while end < len(lines) and not lines[end].startswith("const ") and not lines[end].startswith("/**"):
    end += 1
# 去掉尾部空行
while end > start and lines[end - 1].strip() == "":
    end -= 1

removed = "\n".join(lines[up:end])
assert "LocationSetting" in removed, "anchor wrong"
assert len(removed) < 6000, f"too long: {len(removed)}"
del lines[up:end]

text = "\n".join(lines)
text = text.replace("              <LocationSetting />\n", "")
text = text.replace("import { regionCodes, getRegionName, provinces } from '../../services/location.js'\n", "")
text = text.replace("  setLocation,\n", "")
io.open(p, "w", encoding="utf-8", newline="\n").write(text)
print("removed", len(removed), "chars of LocationSetting")
print("head of removed:", removed.split("\n")[0])
print("tail of removed:", removed.split("\n")[-1])
