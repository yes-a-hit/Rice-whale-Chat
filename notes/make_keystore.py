import io, pathlib, secrets, string, subprocess

root = pathlib.Path(r"E:\flutter\open-deepseek")
alias = "open-deepseek"
jks = root / "android/app/open-deepseek-release.jks"
props = root / "android/keystore.properties"
keytool = r"D:\jdk\bin\keytool.exe"

if not jks.exists():
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for _ in range(24))
    dname = "CN=Open DeepSeek, OU=Mobile, O=Open DeepSeek, L=Local, ST=Local, C=CN"
    subprocess.run(
        [
            keytool, "-genkeypair",
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
    print("keystore ok:", jks)
    print("password:", password)
else:
    print("keystore exists, skip")

# .gitignore
gi = root / ".gitignore"
t = io.open(gi, encoding="utf-8").read() if gi.exists() else ""
add = ["android/keystore.properties", "android/app/*.jks", "android/app/*.keystore"]
missing = [line for line in add if line not in t]
if missing:
    t = t.rstrip("\n") + "\n\n# 签名材料不进仓库\n" + "\n".join(missing) + "\n"
    io.open(gi, "w", encoding="utf-8", newline="\n").write(t)
    print("gitignore ok")
