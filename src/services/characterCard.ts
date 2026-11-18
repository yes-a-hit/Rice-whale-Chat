/**
 * 角色卡（chara card v2 / v3）导入。
 *
 * 支持两种来源：
 *  - JSON 文件：直接的 v2 结构（或 v1 扁平结构）
 *  - PNG 文件：SillyTavern / TavernAI 惯用的 tEXt 块，关键字 `chara`（v2）或 `ccv3`（v3），
 *    内容为 base64 的 JSON
 *
 * 导入后拼成一段系统提示词，交给现有的 system 字段，不改协议。
 */

export type CharacterCard = {
  name: string
  description: string
  personality: string
  scenario: string
  firstMessage: string
  exampleDialogue: string
  systemPrompt: string
  /** 创作者补充说明（v2 的 creator_notes） */
  creatorNotes: string
}

export class CardParseError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'CardParseError'
  }
}

const text = (value: unknown): string => (typeof value === 'string' ? value.trim() : '')

/* eslint-disable @typescript-eslint/no-explicit-any */
const fromObject = (raw: any): CharacterCard => {
  // v2/v3 把字段放在 data 里，v1 是扁平结构
  const data = raw?.data ?? raw
  if (!data || typeof data !== 'object') {
    throw new CardParseError('card has no data')
  }
  const card: CharacterCard = {
    name: text(data.name),
    description: text(data.description),
    personality: text(data.personality),
    scenario: text(data.scenario),
    firstMessage: text(data.first_mes ?? data.first_message ?? data.greeting),
    exampleDialogue: text(data.mes_example ?? data.example_dialogue),
    systemPrompt: text(data.system_prompt),
    creatorNotes: text(data.creator_notes),
  }
  if (!card.name && !card.description) {
    throw new CardParseError('card has neither name nor description')
  }
  return card
}
/* eslint-enable @typescript-eslint/no-explicit-any */

/** 解析 JSON 文本 */
export const parseCardJson = (raw: string): CharacterCard => {
  let parsed: unknown
  try {
    parsed = JSON.parse(raw)
  } catch {
    throw new CardParseError('invalid JSON')
  }
  return fromObject(parsed)
}

const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]

/** 从 PNG 字节里找出角色卡 tEXt 块 */
const extractPngCardText = (bytes: Uint8Array): string | null => {
  for (let i = 0; i < PNG_SIGNATURE.length; i++) {
    if (bytes[i] !== PNG_SIGNATURE[i]) {
      throw new CardParseError('not a PNG file')
    }
  }
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength)
  let offset = 8
  let v2: string | null = null
  let v3: string | null = null
  while (offset + 8 <= bytes.length) {
    const length = view.getUint32(offset)
    const type = String.fromCharCode(...bytes.slice(offset + 4, offset + 8))
    if (type === 'tEXt') {
      const data = bytes.slice(offset + 8, offset + 8 + length)
      const zero = data.indexOf(0)
      if (zero > 0) {
        const keyword = String.fromCharCode(...data.slice(0, zero))
        const value = new TextDecoder('latin1').decode(data.slice(zero + 1))
        if (keyword === 'ccv3') {
          v3 = value
          break
        }
        if (keyword === 'chara') {
          v2 = value
        }
      }
    }
    if (type === 'IEND') {
      break
    }
    offset += 12 + length
  }
  return v3 ?? v2
}

const decodeBase64Utf8 = (value: string): string => {
  const binary = atob(value)
  const bytes = new Uint8Array(binary.length)
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i)
  }
  return new TextDecoder('utf-8').decode(bytes)
}

/** 解析 PNG 角色卡 */
export const parseCardPng = async (file: File): Promise<CharacterCard> => {
  const bytes = new Uint8Array(await file.arrayBuffer())
  const payload = extractPngCardText(bytes)
  if (!payload) {
    throw new CardParseError('PNG has no character card data')
  }
  return parseCardJson(decodeBase64Utf8(payload))
}

/** 按文件类型自动选择解析方式 */
export const parseCardFile = async (file: File): Promise<CharacterCard> =>
  file.name.toLowerCase().endsWith('.png') || file.type === 'image/png'
    ? parseCardPng(file)
    : parseCardJson(await file.text())

/**
 * 把角色卡拼成系统提示词。
 * 只使用卡片本身的信息，不额外添加「你是 AI」这一类会破坏人设的话。
 */
export const buildCardSystemPrompt = (card: CharacterCard): string => {
  const parts: string[] = []
  if (card.systemPrompt) {
    parts.push(card.systemPrompt)
  }
  parts.push(`你现在扮演「${card.name || '角色'}」，始终保持这个身份与说话方式。`)
  if (card.description) {
    parts.push(`角色设定：${card.description}`)
  }
  if (card.personality) {
    parts.push(`性格：${card.personality}`)
  }
  if (card.scenario) {
    parts.push(`场景：${card.scenario}`)
  }
  if (card.exampleDialogue) {
    parts.push(`对话示例（模仿其语气与节奏）：\n${card.exampleDialogue}`)
  }
  return parts.join('\n\n')
}

export type { CharacterCard as Card }
