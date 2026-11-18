import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\chatInput\ChatInput.module.css")
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """  appearance: none;
  cursor: pointer;
}""",
    """  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M1 1l4 4 4-4' fill='none' stroke='%23888' stroke-width='1.5' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 8px center;
  cursor: pointer;
}""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("select arrow ok")
