import io, pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/app/App.tsx"
t = io.open(p, encoding="utf-8").read()

if "previewWelcome" not in t:
    t = t.replace(
        "  const frameRef = useMobileViewport(isMobile)",
        "  // `#preview` 跳过 IndexedDB 等待，直接看欢迎页布局（调试用，不影响正常流程）\n"
        "  const previewWelcome = globalThis.location?.hash === '#preview'\n"
        "  const frameRef = useMobileViewport(isMobile)",
        1,
    )
    old = """            {!ready || (activeId !== null && !session) ? ("""
    new = """            {previewWelcome ? (
              <Welcome />
            ) : !ready || (activeId !== null && !session) ? ("""
    assert old in t
    t = t.replace(old, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("preview hook ok")
