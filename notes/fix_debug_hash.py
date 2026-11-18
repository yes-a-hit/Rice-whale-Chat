import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 调试开关：URL 带 #settings 时直接打开设置（方便无交互截图，也不影响正常使用）
p = root / "src/components/settings/settingsDialogState.ts"
t = io.open(p, encoding="utf-8").read()
if "#settings" not in t:
    t = t.replace(
        "export const useSettingsDialog = create(",
        "/** 打开状态；`#settings` 便于无交互调试时直接进设置页 */\nexport const useSettingsDialog = create(",
        1,
    )
    # 找到 open: false 的初始值
    assert "open: false" in t
    t = t.replace("open: false", "open: globalThis.location?.hash === '#settings'", 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("settings dialog debug hash ok")

# iframe 指向 #settings
p = root / "notes/write_device_frame.py"
t = io.open(p, encoding="utf-8").read()
t = t.replace('<iframe src="/"></iframe>', '<iframe src="/#settings"></iframe>')
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("device frame updated")
