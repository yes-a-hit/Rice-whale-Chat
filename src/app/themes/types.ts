import type { TranslationKey } from '../../i18n/index.js'

/**
 * 主题（Theme）——社区可扩展的视觉包。
 *
 * 一个主题 = 一组主色阶 + 一层装饰 + 可选素材 + 可选自动匹配规则。
 * 只覆盖 `--dsw-static-blue-*` 这类主色变量，不动语义色与布局，
 * 所以任何主题都不会把界面弄成不可用。
 */
export type ThemeId =
  | 'plain'
  | 'ink'
  | 'maid'
  | 'tech'
  | 'sumi'
  | 'moon'
  | 'gyu'

/** 装饰：只影响背景纹理与少量描边，不遮挡内容 */
export type ThemeDecoration = 'none' | 'ink' | 'maid' | 'tech' | 'sumi' | 'moon' | 'gyu'

/** 素材路径，相对于 `/media/`；留空则用默认素材 */
export type ThemeAssets = {
  /** 欢迎页（有 Key）的立绘 */
  welcome?: string
  /** 欢迎页（无 Key）的立绘 */
  hungry?: string
  /** 侧栏与引导页的小图标 */
  logo?: string
}

/**
 * 自动匹配规则：换接口/换模型时自动切主题。
 * 命中顺序：先 model 再 host，都支持子串匹配。
 */
export type ThemeMatchRule = {
  models?: string[]
  hosts?: string[]
}

/**
 * 主色阶：只覆盖 `--dsw-static-blue-50..900`。
 * 用 TS 而不是纯 CSS 存放，是因为套用时要写成行内变量——
 * 行内样式优先级最高，不会被主题选择器匹配不到的情况坑掉。
 */
export type ThemePalette = Record<
  '50' | '100' | '200' | '300' | '400' | '450' | '500' | '600' | '800' | '900',
  string
>

export type Theme = {
  /** 主色阶；省略表示沿用官方配色（plain） */
  palette?: ThemePalette
  /** 立绘自带气泡文字（老素材），为真时不再渲染 DOM 气泡 */
  builtinBubble?: boolean
  /** 装饰底图文件名，位于 /media/；省略表示无装饰 */
  image?: string
  id: ThemeId
  /** 设置界面上显示的名字 */
  nameKey: TranslationKey
  /** 一句话说明，社区作者写清风格来源 */
  descriptionKey?: TranslationKey
  decoration: ThemeDecoration
  assets?: ThemeAssets
  match?: ThemeMatchRule
  /** 作者署名，会显示在主题选择里 */
  author?: string
}

/** 自动匹配用的上下文 */
export type ThemeContext = {
  /** 当前模型 id，比如 deepseek-flash / moonshot-v1-8k / glm-4 */
  model?: string
  /** 聊天服务地址，比如 https://api.moonshot.cn */
  apiBaseUrl?: string
}

const lower = (value: string | undefined) => (value ?? '').toLowerCase()

/**
 * 找出第一个匹配当前接口/模型的主题；没有就返回 null。
 * 规则故意做得很笨：子串匹配，社区作者不用学正则。
 */
export const matchTheme = (themes: Theme[], context: ThemeContext): ThemeId | null => {
  const model = lower(context.model)
  const host = lower(context.apiBaseUrl)
  for (const theme of themes) {
    if (!theme.match) {
      continue
    }
    if (theme.match.models?.some((needle) => model.includes(lower(needle)))) {
      return theme.id
    }
    if (theme.match.hosts?.some((needle) => host.includes(lower(needle)))) {
      return theme.id
    }
  }
  return null
}
