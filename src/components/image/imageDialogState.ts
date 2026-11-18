import { create } from 'zustand'

/** 生图弹窗的开关状态 */
export const useImageDialog = create(() => ({ open: false }))

export const openImageDialog = () => useImageDialog.setState({ open: true })
export const closeImageDialog = () => useImageDialog.setState({ open: false })
