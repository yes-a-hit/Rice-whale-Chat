import { useChatStore } from './chat/store.js'

/**
 * 本地数据库（IndexedDB + CacheStorage）的用量与清理。
 * 会话正文存在 IndexedDB，附件图片与模型走 CacheStorage。
 */

export type LocalStats = {
  /** 会话数 */
  sessions: number
  /** 消息条数 */
  messages: number
  /** 浏览器给出的总占用与配额（字节），不支持时为 null */
  usage: number | null
  quota: number | null
  /** 各 CacheStorage 桶的名字 */
  caches: string[]
}

const formatBytes = (bytes: number): string => {
  if (bytes < 1024) {
    return `${bytes} B`
  }
  const units = ['KB', 'MB', 'GB']
  let value = bytes / 1024
  let index = 0
  while (value >= 1024 && index < units.length - 1) {
    value /= 1024
    index += 1
  }
  return `${value.toFixed(value >= 10 ? 0 : 1)} ${units[index]}`
}

export const formatBytesText = formatBytes

export const readLocalStats = async (): Promise<LocalStats> => {
  const state = useChatStore.getState()
  const sessions = Object.keys(state.sessionCache).length
  let messages = 0
  for (const session of Object.values(state.sessionCache)) {
    messages += session.messages.length
  }
  let usage: number | null = null
  let quota: number | null = null
  try {
    const estimate = await navigator.storage?.estimate?.()
    usage = estimate?.usage ?? null
    quota = estimate?.quota ?? null
  } catch {
    // 隐私模式下拿不到估算
  }
  let cacheNames: string[] = []
  try {
    cacheNames = typeof caches === 'undefined' ? [] : await caches.keys()
  } catch {
    // 忽略
  }
  return { sessions, messages, usage, quota, caches: cacheNames }
}

/** 清掉附件/页面缓存，保留已下载的模型 */
export const clearAttachmentCache = async (): Promise<void> => {
  if (typeof caches === 'undefined') {
    return
  }
  for (const name of await caches.keys()) {
    if (name !== 'ods-models') {
      await caches.delete(name)
    }
  }
}

/** 连模型一起清空 */
export const clearAllCaches = async (): Promise<void> => {
  if (typeof caches === 'undefined') {
    return
  }
  for (const name of await caches.keys()) {
    await caches.delete(name)
  }
}
