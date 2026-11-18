import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\image\ImageDialog.tsx")
t = io.open(p, encoding="utf-8").read()

# 读取弹窗状态里预填的提示词，打开时同步进输入框
t = t.replace(
    "  const open = useImageDialog((state) => state.open)",
    "  const open = useImageDialog((state) => state.open)\n"
    "  const seeded = useImageDialog((state) => state.prompt)",
    1,
)
t = t.replace(
    "  const [prompt, setPrompt] = useState('')",
    "  const [prompt, setPrompt] = useState('')",
    1,
)
# 在 open 变为 true 时填进去：用 useEffect 更稳
t = t.replace(
    "import { useState } from 'react'",
    "import { useEffect, useState } from 'react'",
    1,
)
t = t.replace(
    "  const [error, setError] = useState('')",
    """  const [error, setError] = useState('')

  // 指令触发（/img ...）时预填提示词
  useEffect(() => {
    if (open && seeded) {
      setPrompt(seeded)
    }
  }, [open, seeded])""",
    1,
)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("dialog seed ok")
