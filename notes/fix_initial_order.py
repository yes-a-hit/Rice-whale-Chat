import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\services\settings.ts")
t = io.open(p, encoding="utf-8").read()

block = """/** 模型 id 校验：只认这两个，旧值回落快速档（不引用外部模块，避免初始化顺序问题） */
const initialModel = (): ChatModel =>
  read(KEYS.model) === 'deepseek-v4-pro' ? 'deepseek-v4-pro' : 'deepseek-v4.1-flash'

"""

assert block in t, "block not found"
t = t.replace(block, "", 1)

anchor = "const initialModelSource = (): ModelSource => {"
assert anchor in t
t = t.replace(anchor, block + anchor, 1)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("reordered")
