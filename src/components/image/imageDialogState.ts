import { create } from 'zustand'

/** 生图弹窗：open 控制显示，prompt 是打开时预填的提示词（指令触发用） */
export const useImageDialog = create(() => ({ open: false, prompt: '' }))

export const openImageDialog = (prompt = '') =>
  useImageDialog.setState({ open: true, prompt })

export const closeImageDialog = () => useImageDialog.setState({ open: false, prompt: '' })
