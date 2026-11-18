import type { Theme, ThemeId } from './types.js'

/**
 * 内置主题。新增主题只需在这里加一条 + 在 themes.css 里加配色块，
 * 详见 docs/themes.md。
 */
export const THEMES: Theme[] = [
  {
    id: 'plain',
    nameKey: 'odsThemePlain',
    descriptionKey: 'odsThemePlainDesc',
    decoration: 'none',
    assets: {
      welcome: 'welcome.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
  },
  {
    id: 'ink',
    nameKey: 'odsThemeInk',
    descriptionKey: 'odsThemeInkDesc',
    decoration: 'ink',
    assets: {
      welcome: 'welcome.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
  },
  {
    id: 'maid',
    nameKey: 'odsThemeMaid',
    descriptionKey: 'odsThemeMaidDesc',
    decoration: 'maid',
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
    assets: {
      welcome: 'tech-mascot.webp',
      hungry: 'tech-mascot.webp',
      logo: 'logo-128.webp',
    },
  },
  {
    id: 'sumi',
    nameKey: 'odsThemeSumi',
    descriptionKey: 'odsThemeSumiDesc',
    decoration: 'sumi',
    assets: {
      welcome: 'welcome.webp',
      hungry: 'hungry.webp',
      logo: 'logo-128.webp',
    },
  },
  {
    id: 'moon',
    nameKey: 'odsThemeMoon',
    descriptionKey: 'odsThemeMoonDesc',
    decoration: 'moon',
    // 素材槽留空即回落默认立绘；放 figure/out/moon-mascot.webp 就会自动用上
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
