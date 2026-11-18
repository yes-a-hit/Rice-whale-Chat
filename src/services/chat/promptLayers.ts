import { useSettings } from '../settings.js'

/**
 * 提示词分层注入。
 *
 * 三层，成本从高到低：
 *
 *   1. 系统提示词 + 角色卡   → 每轮都放在 `system` 里（顺序固定：系统在前、角色卡在后）。
 *      这两层是「一直生效」的设定，走 system 才能保证优先级，且能吃到 prompt cache。
 *   2. 辅助提示词（反鲸八股）→ 只在会话首轮注入一条消息，之后随历史滚动；
 *      上下文被压缩后要重新注入一次。这样长规则不会每轮重复计费。
 *   3. 历史后指令           → 跟在辅助提示词后面，同样只在首轮与压缩后出现。
 *
 * 首轮注入用一对 user/assistant 消息包住，避免被模型当成「用户当下的问题」。
 */

/** 首轮注入的标记，用来判断这条会话是否已经注入过 */
export const AUX_MARKER = '【规则层】'

/** 辅助层是否已经有标记落在历史里 */
export const hasAuxInjected = (contents: string[]): boolean =>
  contents.some((text) => text.startsWith(AUX_MARKER))

/** 组装辅助层文本；没有内容或开关关掉时返回空串 */
export const buildAuxBlock = (): string => {
  const { auxEnabled, auxPrompt, tailInstruction } = useSettings.getState()
  if (!auxEnabled) {
    return ''
  }
  const parts = [auxPrompt.trim(), tailInstruction.trim()].filter(Boolean)
  return parts.length > 0 ? `${AUX_MARKER}\n${parts.join('\n\n')}` : ''
}

/** 首轮才注入：历史上没有任何带标记的消息 */
export const shouldInjectAux = (historyContents: string[]): boolean =>
  historyContents.length === 0 || !hasAuxInjected(historyContents)
