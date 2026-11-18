import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\app\themes\themes.css")
t = io.open(p, encoding="utf-8").read()
print("has themes.css content:", "--ods-veil" in t, len(t))
