import io, pathlib, secrets, string, subprocess

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- 1. 版本号 1.0.0-alpha.1 ----------
p = root / "package.json"
t = io.open(p, encoding="utf-8").read()
t = t.replace('"version": "0.1.1"', '"version": "1.0.0-alpha.1"', 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("package.json ->", "1.0.0-alpha.1")

# ---------- 2. build.gradle：版本号驱动 + release 签名 ----------
p = root / "android/app/build.gradle"
t = io.open(p, encoding="utf-8").read()

header = """apply plugin: 'com.android.application'

// ---- 版本号：1.x.y-tag.z，一处定义同时驱动 versionName 与 versionCode ----
def pkgJson = new groovy.json.JsonSlurper().parseText(file('../../package.json').text)
def appVersionName = pkgJson.version as String
def versionMatcher = appVersionName =~ /^(\\d+)\\.(\\d+)\\.(\\d+)(?:-([A-Za-z]+)\\.(\\d+))?$/
if (!versionMatcher.matches()) {
    throw new GradleException("package.json 的 version 必须符合 1.x.y-tag.z，当前：${appVersionName}")
}
def appVersionCode = (versionMatcher.group(1) as int) * 1000000 +
        (versionMatcher.group(2) as int) * 10000 +
        (versionMatcher.group(3) as int) * 100 +
        ((versionMatcher.group(5) ?: '0') as int)

// ---- 签名：android/keystore.properties 存在才用正式签名，否则回退 debug ----
def keystorePropsFile = rootProject.file('keystore.properties')
def keystoreProps = new Properties()
def hasReleaseKey = keystorePropsFile.exists()
if (hasReleaseKey) {
    keystorePropsFile.withInputStream { keystoreProps.load(it) }
}
"""
t = t.replace("apply plugin: 'com.android.application'\n", header, 1)

t = t.replace("        versionCode 1\n        versionName \"1.0\"",
              "        versionCode appVersionCode\n        versionName appVersionName", 1)

t = t.replace("""    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }""",
              """    signingConfigs {
        if (hasReleaseKey) {
            release {
                storeFile rootProject.file(keystoreProps['storeFile'])
                storePassword keystoreProps['storePassword']
                keyAlias keystoreProps['keyAlias']
                keyPassword keystoreProps['keyPassword']
            }
        }
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            if (hasReleaseKey) {
                signingConfig signingConfigs.release
            }
        }
    }""", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("build.gradle patched")

# ---------- 3. 生成 keystore ----------
alias = "open-deepseek"
jks = root / "android/app/open-deepseek-release.jks"
props = root / "android/keystore.properties"

if jks.exists() and props.exists():
    print("keystore 已存在，跳过")
else:
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for _ in range(24))
    dname = "CN=Open DeepSeek, OU=Mobile, O=Open DeepSeek, L=Local, ST=Local, C=CN"
    subprocess.run(
        [
            "keytool", "-genkeypair",
            "-keystore", str(jks),
            "-alias", alias,
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-storepass", password,
            "-keypass", password,
            "-dname", dname,
        ],
        check=True,
    )
    props.write_text(
        "storeFile=app/open-deepseek-release.jks\n"
        f"storePassword={password}\n"
        f"keyAlias={alias}\n"
        f"keyPassword={password}\n",
        encoding="utf-8",
    )
    print("keystore 生成完成")
    print("密码已写入", props)

# ---------- 4. .gitignore ----------
gi = root / ".gitignore"
t = io.open(gi, encoding="utf-8").read() if gi.exists() else ""
add = ["android/keystore.properties", "android/app/*.jks", "android/app/*.keystore"]
missing = [line for line in add if line not in t]
if missing:
    t = t.rstrip("\n") + "\n\n# 签名材料不进仓库\n" + "\n".join(missing) + "\n"
    io.open(gi, "w", encoding="utf-8", newline="\n").write(t)
    print("gitignore ok")
