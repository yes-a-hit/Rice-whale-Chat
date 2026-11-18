import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\billing\SessionStatsBar.tsx")
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    "const replyTextLength = (message: { blocks?: AssistantMessage['blocks'] }): number => {",
    "const replyTextLength = (message: unknown): number => {",
    1,
)
t = t.replace(
    "  for (const block of message.blocks ?? []) {",
    "  const blocks = (message as { blocks?: AssistantMessage['blocks'] }).blocks ?? []\n  for (const block of blocks) {",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
