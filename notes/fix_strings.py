import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\android\app\src\main\res\values\strings.xml")
t = io.open(p, encoding="utf-8").read()
t = t.replace("<string name=\"app_name\">Open DeepSeek</string>", "<string name=\"app_name\">Rice Whale Chat</string>")
t = t.replace("<string name=\"package_name\">com.opendeepseek.chat</string>", "<string name=\"package_name\">com.ricewhale.chat</string>")
t = t.replace("<string name=\"title_activity_main\">Open DeepSeek</string>", "<string name=\"title_activity_main\">Rice Whale Chat</string>")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print(t)
