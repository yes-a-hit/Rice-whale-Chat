import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. package.json 脚本 ----------
p = root / "package.json"
t = io.open(p, encoding="utf-8").read()
if "android:release" not in t:
    t = t.replace(
        '"android:apk": "pnpm build && cap sync android && cd android && gradlew assembleDebug",',
        '"android:apk": "pnpm build && cap sync android && cd android && gradlew assembleDebug",\n'
        '    "android:release": "pnpm build && cap sync android && cd android && gradlew assembleRelease",\n'
        '    "version:bump": "python notes/bump_version.py",',
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("scripts ok")

# ---------- 2. README：版本与签名 ----------
p = root / "README.md"
t = io.open(p, encoding="utf-8").read()
section = """
## 版本与签名

版本号写在 `package.json` 的 `version`，格式固定为 **`1.x.y-tag.z`**：

| 段 | 含义 |
|---|---|
| `1` | 主版本，协议/数据格式大改才动 |
| `x` | 次版本，加功能 |
| `y` | 修订号，修 bug |
| `tag` | `alpha` / `beta` / `rc`，正式版不带 tag |
| `z` | 同一 tag 内的递增序号 |

`android/app/build.gradle` 读这个版本号，同时算出 `versionName` 与 `versionCode`：

```
versionCode = major*1000000 + minor*10000 + patch*100 + tag序号
1.0.0-alpha.1  →  versionCode 1000001
```

日常用脚本改，不用手改：

```bash
pnpm version:bump            # 看当前版本与 versionCode
pnpm version:bump tag        # 1.0.0-alpha.1 -> 1.0.0-alpha.2
pnpm version:bump patch      # -> 1.0.1-alpha.1
pnpm version:bump minor      # -> 1.1.0-alpha.1
pnpm version:bump stable     # -> 1.1.0（正式版）
```

签名材料在 `android/` 下（**不进版本库**）：

- `android/app/open-deepseek-release.jks`：RSA 2048，有效期 10000 天
- `android/keystore.properties`：别名与密码

只要 `keystore.properties` 存在，`assembleRelease` 就自动用正式签名；文件不存在时回退 debug 签名，不影响本地调试。**这两个文件丢了就没法覆盖升级已安装的版本**，务必自己留一份备份。

```bash
pnpm android:release         # 出签名包
# 产物：android/app/build/outputs/apk/release/app-release.apk
```
"""
if "## 版本与签名" not in t:
    t = t.rstrip("\n") + "\n" + section
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("README ok")

# ---------- 3. AUDIT ----------
p = root / "notes/AUDIT-open-deepseek.md"
t = io.open(p, encoding="utf-8").read()
head, _, _ = t.partition("## 状态")
status = """## 状态（2026-11-18 00:34）

### 版本号与签名

- 版本策略 `1.x.y-tag.z` 落在 `package.json` 的 `version`，`android/app/build.gradle` 读取并计算：
  `versionCode = major*1000000 + minor*10000 + patch*100 + tag序号`。
  当前 `1.0.0-alpha.1` → `versionCode 1000001`（已用 `aapt2 dump badging` 核对）。
- 版本工具：`notes/bump_version.py`（`tag` / `patch` / `minor` / `stable` / `alpha|beta|rc`），挂在 `pnpm version:bump`。
- 签名：`notes/make_keystore.py` 用 `D:\\jdk\\bin\\keytool.exe` 生成
  `android/app/open-deepseek-release.jks`（RSA 2048 / 10000 天 / alias `open-deepseek`），
  密码写入 `android/keystore.properties`；两者已加入 `.gitignore`。
- `build.gradle` 里 `signingConfigs.release` 与 `buildTypes.release.signingConfig` 都包在
  `hasReleaseKey` 判断内，缺文件时自动回退 debug 签名。
- 产物：`android/app/build/outputs/apk/release/app-release.apk`（6.7MB），
  `apksigner verify` 通过，证书 SHA-256 `c40dbfd8a21b81f7ef452e6133c345389d3d2c8a5463d4e33cc4334ff78ebfbd`。

### 品牌资源（上一轮）

`figure/` 三张图 → `dist/media/`（构建时复制）：`logo.png` 生成整套 mipmap 与 splash，
`welcome.jpg` / `no-key.jpg` 裁切量化后给欢迎页；引导页与侧栏品牌行也用 `logo-128.png`。

### 手机实测反馈的七条（上一轮）

1. UI 适配（设置弹窗全宽底部面板、修右侧裁切、安全区）
2. 设置入口（顶栏常驻齿轮）
3. 删位置信息
4. 语音可配（语速、系统音色、云端音色）
5. 提示词与角色卡分离
6. 本地数据库（用量统计 + 清理缓存）
7. 余额（`GET /user/balance`）

### 调试脚手架（正常使用不受影响）

`#settings` / `#settings=ext` / `#settings=data` 直开设置分组；`#preview` 跳过 IndexedDB 直接渲染欢迎页；
`python -m http.server 8091 --directory dist` + 390×844 iframe 做手机布局截图。

### 仍未完成

- Kokoro-82M ONNX 推理与中文 G2P（`engines/kokoro.ts` 仍抛 `LOCAL_TTS_NOT_INSTALLED`）
- 原生 NPU 插件（ONNX Runtime Mobile QNN EP）
- 真机实测

## 构建

- 调试：`pnpm android:apk` → `app/build/outputs/apk/debug/app-debug.apk`
- 正式：`pnpm android:release` → `app/build/outputs/apk/release/app-release.apk`
"""
io.open(p, "w", encoding="utf-8", newline="\n").write(head + status)
print("audit ok")
