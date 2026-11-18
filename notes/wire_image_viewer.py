import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")

# 1. MessageFile 用全局查看器
p = root / "src/components/messages/MessageFile.tsx"
t = io.open(p, encoding="utf-8").read()
t = t.replace("onClick={() => onPreview?.(url)}", "onClick={() => openImageViewer(url, file.name)}", 1)
t = t.replace(
    "onOpen={url && !upload ? () => onPreview?.(url) : undefined}",
    "onOpen={url && !upload ? () => openImageViewer(url, file.name) : undefined}",
    1,
)
if "openImageViewer" in t and "imageViewerState" not in t:
    t = t.replace(
        "import styles from './MessageFile.module.css'",
        "import { openImageViewer } from '../files/imageViewerState.js'\nimport styles from './MessageFile.module.css'",
        1,
    )
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("messagefile ok")

# 2. App 根部挂 Host
p = root / "src/app/App.tsx"
t = io.open(p, encoding="utf-8").read()
if "ImageViewerHost" not in t:
    t = t.replace(
        "import { ImageDialog } from '../components/image/ImageDialog.js'",
        "import { ImageDialog } from '../components/image/ImageDialog.js'\nimport { ImageViewerHost } from '../components/files/ImageViewerHost.js'",
        1,
    )
    t = t.replace("<ImageDialog />", "<ImageDialog />\n      <ImageViewerHost />", 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("app host ok")
else:
    print("host already")
