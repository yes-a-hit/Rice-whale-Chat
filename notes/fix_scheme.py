import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\android\app\src\main\res\values\strings.xml")
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    '<string name="custom_url_scheme">com.opendeepseek.chat</string>',
    '<string name="custom_url_scheme">com.ricewhale.chat</string>',
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("scheme ok")
