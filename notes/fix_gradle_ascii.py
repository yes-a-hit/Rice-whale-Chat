import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\android\app\build.gradle")
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    "// ---- 版本号：1.x.y-tag.z，一处定义同时驱动 versionName 与 versionCode ----",
    "// ---- Version: 1.x.y-tag.z in package.json drives both versionName and versionCode ----",
)
t = t.replace(
    'throw new GradleException("package.json 的 version 必须符合 1.x.y-tag.z，当前：${appVersionName}")',
    'throw new GradleException("package.json version must match 1.x.y-tag.z, got: ${appVersionName}")',
)
t = t.replace(
    "// ---- 签名：android/keystore.properties 存在才用正式签名，否则回退 debug ----",
    "// ---- Signing: use release key only when android/keystore.properties exists ----",
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("gradle comments localised to ascii")
