import io, pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\services\chat\store.ts")
t = io.open(p, encoding="utf-8").read()

# 续写：重置耗时计时
old = """    status: 'pending',
    stopReason: undefined,
    stopDetails: undefined,
    error: undefined,
  }"""
new = """    status: 'pending',
    stopReason: undefined,
    stopDetails: undefined,
    error: undefined,
    startedAt: Date.now(),
    elapsedMs: undefined,
  }"""
assert old in t
t = t.replace(old, new, 1)

# 新建回复：同一处模板（第 267 行附近的 createReply）
old2 = """    search,
    prefix: true,
    status: 'pending',
    blocks: [],
  }"""
new2 = """    search,
    prefix: true,
    status: 'pending',
    blocks: [],
    startedAt: Date.now(),
  }"""
assert old2 in t
t = t.replace(old2, new2, 1)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("store timestamps ok")
