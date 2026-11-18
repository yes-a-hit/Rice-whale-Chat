import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# ---------- ReplyArea：完成后按设置自动收起 ----------
p = root / "src/components/messages/ReplyArea.tsx"
t = io.open(p, encoding="utf-8").read()

t = t.replace(
    "  const [open, setOpen] = useState(true)",
    """  const collapseThinking = useSettings((state) => state.collapseThinking)
  const [open, setOpen] = useState(!collapseThinking)
  // 开启「自动折叠」时，流式期间展开（能看见在思考），回答开始/结束后收起
  useEffect(() => {
    if (collapseThinking && !streaming) {
      setOpen(false)
    }
  }, [collapseThinking, streaming])""",
    1,
)

if "import { useSettings }" not in t:
    t = t.replace(
        "import { useTranslate } from '../../i18n/index.js'",
        "import { useTranslate } from '../../i18n/index.js'\nimport { useSettings } from '../../services/settings.js'",
        1,
    )

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("reply area ok")
