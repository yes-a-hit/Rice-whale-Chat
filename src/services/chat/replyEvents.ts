/**
 * 回复完成事件：Lite 模式据此自动朗读。
 * store 不直接依赖朗读模块，避免 chat 层反向依赖 speech 层。
 */

type ReplyDoneListener = (sessionId: string, messageId: string) => void

const listeners = new Set<ReplyDoneListener>()

export const onReplyDone = (listener: ReplyDoneListener): (() => void) => {
  listeners.add(listener)
  return () => {
    listeners.delete(listener)
  }
}

export const emitReplyDone = (sessionId: string, messageId: string) => {
  for (const listener of listeners) {
    try {
      listener(sessionId, messageId)
    } catch {
      // 监听方出错不影响主流程
    }
  }
}
