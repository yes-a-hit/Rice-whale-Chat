import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/app/App.tsx"
t = io.open(p, encoding="utf-8").read()

# 1) 慢加载兜底：3 秒还没就绪就允许手动重载，避免一直转圈
t = t.replace(
    "import { useEffect } from 'react'",
    "import { useEffect, useState } from 'react'",
    1,
)
old = """  usePreventPageScroll(isMobile)"""
new = """  usePreventPageScroll(isMobile)

  // IndexedDB 打不开时不至于永远转圈：给一个手动重载的出口
  const [slowLoad, setSlowLoad] = useState(false)
  useEffect(() => {
    if (ready) {
      return
    }
    const timer = window.setTimeout(() => setSlowLoad(true), 3000)
    return () => window.clearTimeout(timer)
  }, [ready])"""
assert old in t
t = t.replace(old, new, 1)

old = """                  {(!ready ? initError : sessionLoadError) ? (
                    <Button
                      variant="outlined"
                      size="m"
                      onClick={() => {
                        if (!ready) {
                          void initChat()
                        } else if (activeId !== null) {
                          selectSession(activeId)
                        }
                      }}
                    >
                      {t('retry')}
                    </Button>
                  ) : null}"""
new = """                  {(!ready ? initError : sessionLoadError) ? (
                    <Button
                      variant="outlined"
                      size="m"
                      onClick={() => {
                        if (!ready) {
                          void initChat()
                        } else if (activeId !== null) {
                          selectSession(activeId)
                        }
                      }}
                    >
                      {t('retry')}
                    </Button>
                  ) : slowLoad ? (
                    <Button variant="outlined" size="m" onClick={() => location.reload()}>
                      {t('retry')}
                    </Button>
                  ) : null}"""
assert old in t
t = t.replace(old, new, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("slow load fallback ok")
