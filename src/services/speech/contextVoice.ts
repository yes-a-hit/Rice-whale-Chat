/**
 * 进阶 TTS：按上下文挑音色与语速（实验性）。
 *
 * 系统语音的音色由设备决定，能调的其实只有「用哪个 voice + 语速 + 音高」。
 * 这里用一套可解释的规则判断回复的语气，再给出这三项参数：
 *
 *   - 问句多、结尾是问号        → 语速稍慢，音高略低（像在解释）
 *   - 感叹号密集、短句          → 语速稍快，音高略高（有情绪）
 *   - 长段落、书面语            → 语速正常偏慢，音高中性
 *   - 代码 / 表格 / 链接密集    → 慢一点，避免数字念飞
 *   - 列表、步骤                → 每项之间多留停顿（rate 略慢）
 *
 * 不做「一个 voice 演多角色」那种事——Web Speech 只给一份 voice 列表，
 * 硬要区分角色反而更假。
 */

export type VoiceProfile = {
  /** 匹配到的场景，界面上可以显示 */
  mood: 'question' | 'excited' | 'code' | 'list' | 'calm'
  rate: number
  pitch: number
}

const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value))

/** 从正文推断语气，base 为用户设置的基准语速 */
export const matchVoiceProfile = (text: string, baseRate: number): VoiceProfile => {
  const body = text.trim()
  const length = body.length
  const codeLines = (body.match(/^\s*(```|>|\||\$ |const |function |import |def |class )/gm) ?? []).length
  const listLines = (body.match(/^\s*([-*+]|\d+[.)])\s+/gm) ?? []).length
  const questions = (body.match(/[？?]/g) ?? []).length
  const exclaims = (body.match(/[！!]/g) ?? []).length
  const digits = (body.match(/[0-9]/g) ?? []).length

  if (codeLines > 0 || digits / Math.max(1, length) > 0.15) {
    return { mood: 'code', rate: clamp(baseRate * 0.92, 0.5, 2), pitch: 1 }
  }
  if (exclaims >= 2 && length < 120) {
    return { mood: 'excited', rate: clamp(baseRate * 1.08, 0.5, 2), pitch: 1.06 }
  }
  if (questions > 0 && questions >= exclaims) {
    return { mood: 'question', rate: clamp(baseRate * 0.96, 0.5, 2), pitch: 0.97 }
  }
  if (listLines >= 3) {
    return { mood: 'list', rate: clamp(baseRate * 0.95, 0.5, 2), pitch: 1 }
  }
  return { mood: 'calm', rate: clamp(baseRate, 0.5, 2), pitch: 1 }
}

/** 朗读前清掉不适合念的东西：代码块、表格、URL */
export const stripUnreadable = (text: string): string =>
  text
    .replace(/```[\s\S]*?```/g, '，这里有一段代码，先跳过。')
    .replace(/^\s*\|.*\|\s*$/gm, '')
    .replace(/https?:\/\/\S+/g, '一个链接')
    .replace(/\s{2,}/g, ' ')
    .trim()
