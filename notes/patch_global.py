import io, shutil, datetime, pathlib, sys

p = pathlib.Path(r"C:\Users\doubl\AppData\Roaming\dsh-desktop\harness\prompt-inject.md")
raw = p.read_bytes()
text = None
for enc in ("utf-8", "utf-8-sig", "gbk"):
    try:
        text = raw.decode(enc)
        print("decoded with", enc, "chars", len(text))
        break
    except UnicodeDecodeError:
        continue
if text is None:
    sys.exit("cannot decode prompt-inject.md")

marker = "## 本机硬约束（全局）"
if marker in text:
    print("already present, skip")
    sys.exit(0)

stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
shutil.copy2(p, p.with_suffix(f".md.bak-{stamp}"))
print("backup:", p.with_suffix(f".md.bak-{stamp}"))

block = """

---

## 本机硬约束（全局，2026-11-18 由主人下达）

**不要开 Android 模拟器调试。** `emulator.exe` / AVD（如 `RPClient_API36`）/ `qemu-system-*` 会拖死本机。

需要验证 Android 产物时，只走这三条：
1. 出包（`pnpm android:apk` / `gradlew assembleDebug`）后交给主人装真机测试；
2. 用 `adb devices` 确认有真机连接，再 `adb install -r`；
3. UI 逻辑在浏览器 `pnpm dev` 里验证（不涉及原生桥）。

如果发现模拟器进程在跑，立刻 `Stop-Process -Name emulator,qemu-system-x86_64 -Force` 清掉。

**改含中文的源文件**：用 Python `io.open(..., encoding='utf-8')` 读写，不要用 PowerShell `Get-Content | Set-Content -Encoding utf8`（会按 ANSI 解码毁掉 UTF-8）。PowerShell 内联多行 `python -c` 会被解析器吃掉，写成 `.py` 文件再执行。
"""

if not text.endswith("\n"):
    text += "\n"
text += block
io.open(p, "w", encoding="utf-8", newline="\n").write(text)
print("appended", len(block), "chars; total now", len(text))
