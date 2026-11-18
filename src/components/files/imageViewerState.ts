import { create } from 'zustand'

/** 应用内图片查看器的全局状态：任意组件 open(url)，由 ImageViewerHost 统一渲染 */
export const useImageViewer = create<{ src: string | null; alt?: string }>(() => ({ src: null }))

export const openImageViewer = (src: string, alt?: string) =>
  useImageViewer.setState({ src, alt })

export const closeImageViewer = () => useImageViewer.setState({ src: null })
