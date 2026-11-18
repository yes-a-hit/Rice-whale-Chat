import io
import pathlib

path = pathlib.Path(r"E:\flutter\open-deepseek\src\components\base\icons.tsx")
t = io.open(path, encoding="utf-8").read()

if "IconFolderOutline16" not in t:
    t = t.rstrip() + """

/** 文件夹：归档用 */
export const IconFolderOutline16 = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
    <path
      d="M2 4.2c0-.66.54-1.2 1.2-1.2h2.3c.43 0 .83.23 1.04.6l.5.86h5.76c.66 0 1.2.54 1.2 1.2v6.14c0 .66-.54 1.2-1.2 1.2H3.2A1.2 1.2 0 0 1 2 11.8V4.2Z"
      stroke="currentColor"
      strokeWidth="1.4"
      strokeLinejoin="round"
    />
  </svg>
)
"""
    io.open(path, "w", encoding="utf-8", newline="\n").write(t)
    print("icon added")
