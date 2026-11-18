import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\base\icons.tsx")
t = io.open(p, encoding="utf-8").read()

if "IconChartOutline16" not in t:
    icon = """
export const IconChartOutline16 = () => (
  <svg width={16} height={16} viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x={2.2} y={9.2} width={2.8} height={4.6} rx={0.9} stroke="currentColor" strokeWidth={1.3} />
    <rect x={6.6} y={6.2} width={2.8} height={7.6} rx={0.9} stroke="currentColor" strokeWidth={1.3} />
    <rect x={11} y={2.2} width={2.8} height={11.6} rx={0.9} stroke="currentColor" strokeWidth={1.3} />
  </svg>
)
"""
    t = t.rstrip("\n") + "\n" + icon
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("icon added")

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\settings\SettingsDialog.tsx")
t = io.open(p, encoding="utf-8").read()
if "IconChartOutline16" not in t.split("\n")[0:20].__str__():
    t = t.replace(
        "  IconDataOutline16,",
        "  IconChartOutline16,\n  IconDataOutline16,",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("import ok")
