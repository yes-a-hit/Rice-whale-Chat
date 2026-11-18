import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\messages\AssistantMessage.tsx")
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    "      {!streaming && !refused && view.searchResults.length > 0 ? (",
    "      {!streaming && view.searchResults.length > 0 ? (",
    1,
)
t = t.replace(
    "            {responseText && !refused ? (",
    "            {responseText ? (",
    1,
)
t = t.replace(
    "              disabled={busy || refused}",
    "              disabled={busy}",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("refused leftovers removed")
