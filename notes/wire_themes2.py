import io
import pathlib

root = pathlib.Path(r"E:\flutter\open-deepseek")
p = root / "src/components/settings/ExtSettings.tsx"
t = io.open(p, encoding="utf-8").read()

# 主题选择：换成主题注册表 + 自动匹配开关
old = """      <SettingCell
        label={t('odsSkin')}
        description={t('odsSkinHint')}
        status={null}
        action={
          <Select<SkinId>
            ariaLabel={t('odsSkin')}
            value={(SKINS.some((item) => item.id === skin) ? skin : 'deepseek') as SkinId}
            options={SKINS.map((item) => ({
              value: item.id,
              label: t(item.labelKey),
            }))}
            onChange={setSkin}
          />
        }
      />"""
new = """      <SettingCell
        label={t('odsTheme')}
        description={t('odsThemeHint')}
        status={null}
        action={
          <Select<ThemeId>
            ariaLabel={t('odsTheme')}
            value={isThemeId(skin) ? skin : 'plain'}
            options={THEMES.map((item) => ({
              value: item.id,
              label: t(item.nameKey),
            }))}
            onChange={setSkin}
          />
        }
      />
      <SettingCell
        label={t('odsThemeAuto')}
        description={t('odsThemeAutoHint')}
        status={null}
        action={
          <button
            type="button"
            role="switch"
            aria-checked={themeAuto}
            className={clsx(styles.switch, themeAuto && styles.switchOn)}
            onClick={() => setThemeAuto(!themeAuto)}
          >
            <span className={styles.switchThumb} />
          </button>
        }
      />"""
assert old in t
t = t.replace(old, new, 1)

t = t.replace(
    "  const skin = useSettings((state) => state.skin)",
    "  const skin = useSettings((state) => state.skin)\n  const themeAuto = useSettings((state) => state.themeAuto)",
    1,
)
t = t.replace(
    "import { SKINS, type SkinId } from '../../app/skins.js'",
    "import { isThemeId, THEMES } from '../../app/themes/registry.js'\nimport type { ThemeId } from '../../app/themes/types.js'",
    1,
)
t = t.replace("  setSkin,", "  setSkin,\n  setThemeAuto,", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("theme selector ok")

# Web Speech 相关的皮肤 key 改名：补 i18n
p = root / "src/i18n/zh.ts"
t = io.open(p, encoding="utf-8").read()
if "odsThemePlain" not in t:
    pairs = [
        ("odsTheme", "主题"),
        ("odsThemeHint", "换配色与背景装饰，不影响布局"),
        ("odsThemeAuto", "跟随接口自动换主题"),
        ("odsThemeAutoHint", "识别到 kimi → 月兔，glm → 奶牛；手动选择优先于自动"),
        ("odsThemePlain", "最简（原版）"),
        ("odsThemePlainDesc", "官方配色，无装饰"),
        ("odsThemeInk", "国风"),
        ("odsThemeInkDesc", "青蓝水墨，鲸鱼娘立绘"),
        ("odsThemeMaid", "经典女仆"),
        ("odsThemeMaidDesc", "深蓝白蕾丝，女仆装鲸鱼娘"),
        ("odsThemeTech", "科技"),
        ("odsThemeTechDesc", "青蓝荧光网格，机能风鲸鱼娘"),
        ("odsThemeSumi", "水墨"),
        ("odsThemeSumiDesc", "墨色留白，黑鲸鱼"),
        ("odsThemeMoon", "月兔（Kimi）"),
        ("odsThemeMoonDesc", "米白淡紫，月兔与水兔女郎"),
        ("odsThemeGyu", "奶牛（GLM）"),
        ("odsThemeGyuDesc", "黑白奶牛斑，萝莉牛娘"),
    ]
    block = "".join(f"  {k}: '{v}',\n" for k, v in pairs)
    t = t.replace("} as const", block + "} as const", 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("zh theme keys ok")

p = root / "src/i18n/en.ts"
t = io.open(p, encoding="utf-8").read()
if "odsThemePlain" not in t:
    pairs = [
        ("odsTheme", "Theme"),
        ("odsThemeHint", "Palette and background only, layout untouched"),
        ("odsThemeAuto", "Pick theme from endpoint"),
        ("odsThemeAutoHint", "kimi to Moon Rabbit, glm to Cow; manual choice wins"),
        ("odsThemePlain", "Plain (original)"),
        ("odsThemePlainDesc", "Official palette"),
        ("odsThemeInk", "Ink"),
        ("odsThemeInkDesc", "Teal ink wash"),
        ("odsThemeMaid", "Classic Maid"),
        ("odsThemeMaidDesc", "Navy and white lace"),
        ("odsThemeTech", "Tech"),
        ("odsThemeTechDesc", "Cyan grid and neon"),
        ("odsThemeSumi", "Sumi"),
        ("odsThemeSumiDesc", "Black ink minimal"),
        ("odsThemeMoon", "Moon Rabbit (Kimi)"),
        ("odsThemeMoonDesc", "Cream and lilac"),
        ("odsThemeGyu", "Cow (GLM)"),
        ("odsThemeGyuDesc", "Black and white spots"),
    ]
    block = "".join(f"  {k}: '{v}',\n" for k, v in pairs)
    t = t.replace("} satisfies Record<keyof typeof zh, string>", block + "} satisfies Record<keyof typeof zh, string>", 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("en theme keys ok")
