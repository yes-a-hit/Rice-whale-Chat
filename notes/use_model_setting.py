import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# store：模型从设置读，不再用常量
p = root / "src/services/chat/store.ts"
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """/** deepseek-flash 同时支持深度思考与图片输入 */
const MODEL: ChatModel = 'deepseek-flash'""",
    """/** 当前模型由设置决定（Lite 快速/专家两档，Plus 可任选） */
const currentModel = (): ChatModel => useSettings.getState().model""",
    1,
)
t = t.replace("model: MODEL,", "model: currentModel(),")
t = t.replace("model: previous.model ?? MODEL,", "model: previous.model ?? currentModel(),")
t = t.replace("model: initial.model ?? MODEL,", "model: initial.model ?? currentModel(),")
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("store ok")
