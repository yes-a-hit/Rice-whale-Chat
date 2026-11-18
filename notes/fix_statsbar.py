import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\billing\SessionStatsBar.tsx")
t = io.open(p, encoding="utf-8").read()
t = t.replace(
    """import {
  compactNumber,
  formatCost,
  summarizeUsage,
  type PriceTable,
} from '../../services/billing.js'""",
    """import { compactNumber, formatCost, summarizeUsage } from '../../services/billing.js'""",
)
t = t.replace(
    """  const price = useSettings((state) => (state as unknown as { price?: PriceTable }).price)

  const usage = useMemo(
    () => summarizeUsage(session?.messages ?? [], price),
    [session?.messages, price]
  )""",
    """  const usage = useMemo(() => summarizeUsage(session?.messages ?? []), [session?.messages])""",
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("statsbar cleaned")
