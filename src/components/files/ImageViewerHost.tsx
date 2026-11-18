import { ImageViewer } from './ImageViewer.js'
import { closeImageViewer, useImageViewer } from './imageViewerState.js'

/** 挂在 App 根部：有 src 时铺一层全屏查看器 */
export const ImageViewerHost = () => {
  const src = useImageViewer((state) => state.src)
  const alt = useImageViewer((state) => state.alt)
  if (!src) {
    return null
  }
  return <ImageViewer src={src} alt={alt} onClose={closeImageViewer} />
}
