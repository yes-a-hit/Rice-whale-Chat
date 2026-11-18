import type { Theme, ThemeId } from './types.js'

/**
 * 内置主题。新增主题只需在这里加一条（调色板 + 可选装饰图 + 可选素材），
 * 详见 docs/themes.md。
 *
 * 配色为什么在 TS 而不在 CSS：套用时写成行内变量（`root.style.setProperty`），
 * 行内样式优先级最高，主题一定生效；CSS 里只留遮罩这类结构性样式。
 */
export const THEMES: Theme[] = [
  {
    id: 'plain',
    nameKey: 'odsThemePlain',
    descriptionKey: 'odsThemePlainDesc',
    decoration: 'none',
    // 不设 palette：沿用官方 DeepSeek 蓝紫
    assets: {
      welcome: 'plain-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
  },
  {
    id: 'ink',
    nameKey: 'odsThemeInk',
    descriptionKey: 'odsThemeInkDesc',
    decoration: 'ink',
    image: 'decor-ink.webp',
    palette: {
      '50': '#edf7f6',
      '100': '#d3ecea',
      '200': '#aadbd7',
      '300': '#78c2bd',
      '400': '#4ea7a3',
      '450': '#38918e',
      '500': '#2f7d84',
      '600': '#22646b',
      '800': '#16474d',
      '900': '#0e3438',
    },
    // 汉服鲸鱼女仆是国风的主角
    assets: {
      welcome: 'ink-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
  },
  {
    id: 'maid',
    nameKey: 'odsThemeMaid',
    descriptionKey: 'odsThemeMaidDesc',
    decoration: 'maid',
    image: 'decor-maid.webp',
    palette: {
      '50': '#edeff8',
      '100': '#d6dcf0',
      '200': '#b3bfe0',
      '300': '#8b9ccb',
      '400': '#6478b0',
      '450': '#4f629b',
      '500': '#3b4f8a',
      '600': '#2c3d70',
      '800': '#1e2a4d',
      '900': '#141c35',
    },
    assets: {
      welcome: 'maid-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
  },
  {
    id: 'tech',
    nameKey: 'odsThemeTech',
    descriptionKey: 'odsThemeTechDesc',
    decoration: 'tech',
    image: 'decor-tech.webp',
    palette: {
      '50': '#e4fbff',
      '100': '#c0f4ff',
      '200': '#8fe9ff',
      '300': '#57d8fb',
      '400': '#1fc2ee',
      '450': '#00a6d6',
      '500': '#0093c4',
      '600': '#00769e',
      '800': '#00536f',
      '900': '#003b50',
    },
    assets: {
      welcome: 'tech-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
  },
  {
    id: 'sumi',
    nameKey: 'odsThemeSumi',
    descriptionKey: 'odsThemeSumiDesc',
    decoration: 'sumi',
    image: 'decor-sumi.webp',
    palette: {
      '50': '#f6f6f5',
      '100': '#e6e6e3',
      '200': '#cfceca',
      '300': '#adaba5',
      '400': '#8a877f',
      '450': '#6f6c65',
      '500': '#4a4a48',
      '600': '#35352f',
      '800': '#1e1e1b',
      '900': '#111110',
    },
    assets: {
      welcome: 'sumi-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
  },
  {
    id: 'moon',
    nameKey: 'odsThemeMoon',
    descriptionKey: 'odsThemeMoonDesc',
    decoration: 'moon',
    image: 'decor-moon.webp',
    palette: {
      '50': '#f6f3ff',
      '100': '#e9e2ff',
      '200': '#d8ccff',
      '300': '#bda9f7',
      '400': '#a288ea',
      '450': '#9478de',
      '500': '#8a6fd6',
      '600': '#6c53b4',
      '800': '#4a387c',
      '900': '#302453',
    },
    assets: {
      welcome: 'moon-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
    match: {
      models: ['kimi', 'moonshot'],
      hosts: ['moonshot', 'kimi'],
    },
  },
  {
    id: 'gyu',
    nameKey: 'odsThemeGyu',
    descriptionKey: 'odsThemeGyuDesc',
    decoration: 'gyu',
    image: 'decor-gyu.webp',
    palette: {
      '50': '#eff5fa',
      '100': '#d9e7f2',
      '200': '#b9d2e6',
      '300': '#92b6d4',
      '400': '#6b99bd',
      '450': '#557fa4',
      '500': '#4a6f8f',
      '600': '#395872',
      '800': '#253c50',
      '900': '#182938',
    },
    assets: {
      welcome: 'gyu-mascot.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
    match: {
      models: ['glm', 'chatglm', 'zhipu'],
      hosts: ['bigmodel', 'zhipu'],
    },
  },
]

export const DEFAULT_THEME: ThemeId = 'plain'

export const isThemeId = (value: string): value is ThemeId =>
  THEMES.some((theme) => theme.id === value)

export const themeById = (id: ThemeId): Theme => THEMES.find((theme) => theme.id === id) ?? THEMES[0]

/** 素材地址：统一走 /media/，缺省回落到默认图 */
export const themeAsset = (id: ThemeId, key: 'welcome' | 'hungry' | 'logo'): string => {
  const theme = themeById(id)
  const file = theme.assets?.[key] ?? THEMES[0].assets?.[key]
  return `/media/${file}`
}
