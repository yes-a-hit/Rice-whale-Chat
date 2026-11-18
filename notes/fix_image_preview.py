import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\src\components\messages\MessageFile.tsx")
t = io.open(p, encoding="utf-8").read()

# 1. 图片正常态：改成按钮 + 应用内查看器，不再新开页面
old_a = """    // 正常态：链接到原件
    return url ? (
      <a
        className={clsx(styles.image, styles.imageThumb)}
        href={url}
        target="_blank"
        rel="noreferrer"
        title={file.name}
      >
        {preview}
      </a>
    ) : ("""
new_a = """    // 正常态：点开走应用内查看器（原来 window.open 会开一个没尺寸约束的新页面）
    return url ? (
      <button
        type="button"
        className={clsx(styles.image, styles.imageThumb)}
        title={file.name}
        aria-label={file.name}
        onClick={() => onPreview?.(url)}
      >
        {preview}
      </button>
    ) : ("""
assert old_a in t
t = t.replace(old_a, new_a, 1)

# 2. 非图片文件：同样走查看器（图片类），其余保持不打开
t = t.replace(
    "      onOpen={url && !upload ? () => window.open(url, '_blank', 'noreferrer') : undefined}",
    "      onOpen={url && !upload ? () => onPreview?.(url) : undefined}",
    1,
)

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("message file ok")
