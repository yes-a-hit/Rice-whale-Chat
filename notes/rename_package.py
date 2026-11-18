import io
import pathlib
import shutil

root = pathlib.Path(r"E:\flutter\open-deepseek")

OLD = "com.opendeepseek.chat"
NEW = "com.ricewhale.chat"

# 1. capacitor.config.json
p = root / "capacitor.config.json"
t = io.open(p, encoding="utf-8").read()
t = t.replace(f'"appId": "{OLD}"', f'"appId": "{NEW}"')
io.open(p, "w", encoding="utf-8", newline="\n").write(t)

# 2. build.gradle
p = root / "android/app/build.gradle"
t = io.open(p, encoding="utf-8").read()
t = t.replace(f'namespace "{OLD}"', f'namespace "{NEW}"')
t = t.replace(f'applicationId "{OLD}"', f'applicationId "{NEW}"')
io.open(p, "w", encoding="utf-8", newline="\n").write(t)

# 3. MainActivity 换包目录
old_dir = root / "android/app/src/main/java/com/opendeepseek/chat"
new_dir = root / "android/app/src/main/java/com/ricewhale/chat"
new_dir.mkdir(parents=True, exist_ok=True)

src = old_dir / "MainActivity.java"
dst = new_dir / "MainActivity.java"
t = io.open(src, encoding="utf-8").read()
t = t.replace(f"package {OLD};", f"package {NEW};")
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
shutil.rmtree(root / "android/app/src/main/java/com/opendeepseek")

print("java:", dst.exists())
print("old removed:", not (root / "android/app/src/main/java/com/opendeepseek").exists())
print((root / "android/app/build.gradle").read_text(encoding="utf-8").count(NEW), "refs in gradle")
