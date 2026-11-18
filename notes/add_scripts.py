import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\package.json")
t = io.open(p, encoding="utf-8").read()

old = '"android:open": "cap open android",'
new = (
    '"android:release": "pnpm android:sync && cd android && gradlew.bat assembleRelease",\n'
    '    "android:open": "cap open android",\n'
    '    "version:bump": "python notes/bump_version.py",'
)
if "android:release" not in t:
    assert old in t
    t = t.replace(old, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("scripts added")
else:
    print("already present")
