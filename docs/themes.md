# 主题（Theme）

主题是纯视觉包：**换主色 + 换背景装饰 + 可选换立绘**，不动布局、不动语义色、不动交互。
所以任何主题都不会把界面弄坏，社区作者也不需要读整个前端。

代码位置：

```
src/app/themes/
  types.ts      主题类型与自动匹配规则
  registry.ts   内置主题清单
  themes.css    配色与装饰
src/app/skins.ts  套用逻辑（applyAppearance / selectTheme）
```

---

## 1. 一个主题长什么样

```ts
{
  id: 'ink',
  nameKey: 'odsThemeInk',            // 设置里的显示名
  descriptionKey: 'odsThemeInkDesc', // 可选，一句话说明
  decoration: 'ink',                 // 对应 themes.css 里的装饰
  assets: {
    welcome: 'welcome.webp',         // 有 API Key 时的欢迎页立绘
    hungry: 'hungry.webp',           // 没有 Key 时的立绘
    logo: 'logo-128.webp',           // 侧栏与引导页的小图标
  },
  match: {                           // 可选：自动匹配
    models: ['kimi', 'moonshot'],
    hosts: ['moonshot'],
  },
}
```

素材路径相对 `dist/media/`，源文件在 `figure/out/`，构建时由 rspack 的 `CopyRspackPlugin` 拷进去。

---

## 2. 新增一个主题

### 第一步：配色

在 `src/app/themes/themes.css` 加一段，覆盖 10 个主色阶：

```css
html[data-theme='mytime'] {
  --dsw-static-blue-50:  #f5f7ff;
  --dsw-static-blue-100: #e4e9ff;
  --dsw-static-blue-200: #c9d3ff;
  --dsw-static-blue-300: #a3b4fb;
  --dsw-static-blue-400: #7d90f0;
  --dsw-static-blue-450: #6273e0;
  --dsw-static-blue-500: #4b5ac4;
  --dsw-static-blue-600: #39459c;
  --dsw-static-blue-800: #262f6e;
  --dsw-static-blue-900: #1a2149;
}
```

只需要这十个变量。它们喂给 `--dsw-alias-*` 那一层，按钮、链接、选中态、进度条会自动跟着变。

> **不要**改 `--dsw-alias-bg-base`、`--dsw-alias-label-primary` 这类语义色。
> 语义色同时被深色模式、对比度、可读性依赖，改了就会出现「白字白底」。

### 第二步：背景装饰（可选）

在同一个选择器里加一行 `--ods-decor`，它的值会被拼到 `.frame` 的 `background-image` 上：

```css
  --ods-decor: radial-gradient(120% 60% at 12% -10%, rgba(75, 90, 196, 0.16), transparent 60%);
```

可以叠多层渐变（见 `tech` 主题的网格写法）。装饰只是背景，**不占 DOM、不接事件、不会挡点击**。

### 第三步：立绘（可选）

把图放进 `figure/out/`，命名 `<主题id>-mascot.webp`，尺寸建议宽 520–760px、透明底、WEBP 质量 82–86。
没放就回落默认立绘，不会报错。

### 第四步：注册

在 `src/app/themes/registry.ts` 的 `THEMES` 里加一条，并在 `ThemeId` 联合类型里加上这个 id：

```ts
export type ThemeId = 'plain' | 'ink' | 'maid' | 'tech' | 'sumi' | 'moon' | 'gyu' | 'mytime'
```

---

## 3. 自动跟随接口

`matchTheme()` 用**子串匹配**，不做正则，社区作者不用学语法：

```ts
match: {
  models: ['kimi', 'moonshot'],   // 模型 id 含这些词的命中
  hosts: ['moonshot', 'kimi'],    // 聊天服务地址含这些词的命中
}
```

判断顺序：先比 `models`，再比 `hosts`，命中第一个就停。当前只拿得到 `apiBaseUrl`，
所以 `hosts` 是最可靠的判据：

| 服务 | 地址片段 | 主题 |
|---|---|---|
| Kimi / Moonshot | `api.moonshot.cn` | `moon` 月兔（米白淡紫，水兔女郎） |
| 智谱 GLM | `open.bigmodel.cn` | `gyu` 奶牛（黑白斑，萝莉牛娘） |

设置里有开关「跟随接口自动换主题」。**手动选择的优先级高于自动**——只有开关打开时才会被覆盖。

---

## 4. 内置主题

| id | 名称 | 主色 | 装饰 | 立绘 |
|---|---|---|---|---|
| `plain` | 最简（原版） | 官方蓝 | 无 | 国风鲸鱼娘 |
| `ink` | 国风 | 青蓝 | 水墨晕染 | 国风鲸鱼娘 |
| `maid` | 经典女仆 | 深蓝白 | 蕾丝斜纹 | 女仆装鲸鱼娘 |
| `tech` | 科技 | 青蓝荧光 | 网格 + 光束 | 机能风鲸鱼娘 |
| `sumi` | 水墨 | 墨黑 | 墨色留白 | 国风鲸鱼娘 |
| `moon` | 月兔（Kimi） | 米白淡紫 | 月晕 | 待补 |
| `gyu` | 奶牛（GLM） | 黑白蓝 | 奶牛斑 | 待补 |

---

## 5. 接口稳定性

下面这些是**公开契约**，改它们算破坏性变更：

- `Theme` 类型的字段名与语义（只增不改）
- `themes.css` 里对 `--dsw-static-blue-*` 的使用
- `--ods-decor` 变量的语义
- 素材目录 `figure/out/` 与命名 `<id>-mascot.webp`
- `matchTheme()` 的子串匹配语义

不保证稳定的：内部实现、`decoration` 的具体取值（随时可能新增）、是否使用某个 CSS 变量。

---

## 6. 装饰底图（decor）

每套主题可以带一张背景纹理，放在 `src/app/themes/assets/decor-<id>.webp`（1024 见方出图，缩到 640 再存，约 4–20 KB）。

CSS 里这样用：

```css
  --ods-decor: linear-gradient(rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0.92)),
    url('./assets/decor-tech.webp');
```

第一层是白色遮罩，把底图压到「隐约可见」。**遮罩透明度就是这个主题的气质**：

| 透明度 | 观感 | 适合 |
|---|---|---|
| 0.80–0.85 | 纹理明显 | 山水、墨迹这种本来就淡的图 |
| 0.86–0.90 | 隐约 | 大多数主题 |
| 0.92–0.97 | 几乎只是纸纹 | 高对比图案（奶牛斑、电路） |

低于 0.78 就开始影响文字对比度了，别越线。

### 出图

本机用 ComfyUI + moss 模型批量出，脚本 `notes/run_moss.py`：

```bash
python notes/run_moss.py            # 全部主题
python notes/run_moss.py ink tech   # 指定主题
```

工作流存了一份在 `notes/moss-decor-workflow.json`（8 步、1024×1024、负向词禁文字与人）。
依赖：ComfyUI 在 8188 运行，且 `extra_model_paths.yaml` 指向共享模型目录。

提示词写法：一段风格描述 + `seamless background texture for a chat app, subtle and low contrast,
soft gradients, no characters, no text, plenty of calm empty space`。
**明确写 no characters**，否则模型一定会塞人进去。
