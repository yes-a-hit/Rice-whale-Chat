import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\billing\SessionStatsBar.tsx")
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    """/** 粗略取一条回复已生成的正文长度（不含思考块） */
const replyTextLength = (message: AssistantMessage): number => {""",
    """/** 粗略取一条回复已生成的正文长度（不含思考块） */
const replyTextLength = (message: { blocks?: AssistantMessage['blocks'] }): number => {""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
