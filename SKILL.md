---
name: "personal-profile-builder"
description: "一键生成个人扩列条HTML页面。用户用自然语言描述自己，自动转换为精美网页。"
---
# 个人扩列条生成器

## 功能简介

帮助用户快速创建精美的个人扩列条网页。用户用自然语言描述自己，系统自动转换为JSON配置并生成HTML页面。

> 视觉效果已大幅优化：所有组件阴影自动跟随主题色、弹窗细节精致化、夜间模式全面覆盖无死角。

## 使用流程

1. 用户用自然语言描述扩列条内容
2. 系统分析内容并识别缺失信息
3. 向用户询问缺失的字段（头像、配色方案、暗号词等），配色优先展示 8 套预设供选择
4. 运行生成脚本，输出最终HTML文件

## 目录结构

```
personal-profile-builder/
├── SKILL.md (此文件)
├── scripts/
│   └── generate.py    # HTML生成脚本
├── assets/
│   ├── basic-styles.css
│   ├── script.js
│   └── config.json    # 参考配置模板
└── references/        # 参考文档（可选）
```

## 工作步骤

### 第一步：理解用户需求

让用户用自然语言描述他的扩列条，例如：

> "我叫小明，性格活泼开朗，喜欢玩游戏和画画，来自北京。"

### 第二步：生成JSON配置

将用户描述转换为JSON配置，严格遵循以下规则：

**基础规则：**

- 只提取用户明确提到的信息，不要编造
- toc包含三个部分：
  - overview（概述）— 详见下方"概述规则"
  - friendship（个人扩列条，核心内容）
  - personal_media（个人媒体，仅在有链接或图片时添加）
- header包含title和subtitle
- display包含version（默认"2.0"）和update_date（默认当前年份）

**概述规则：**
overview 是整个全文的**高度凝练的总结**，不是原话复制。它应该用一两句话概括用户的核心身份标签：名字、性格、关键爱好、来自哪里、扩列诉求。如果用户明确提供了"简洁版扩列条"或"一句话介绍"，可直接使用。

- 正确示例：用户长篇描述了狼设、世界设定、多种爱好 → overview 应提炼为 "一只来自虹九宇宙的黄色小狼，INTJ-A，性格包容而抽象，热爱世界观创作，期待与您扩列～"
- 错误示例：直接复制 friendship 中 OC介绍 的第一段话

**蓝名直达规则：**
当用户提到"蓝名直达 @XXX"时，说明他需要为这个社交账号提供一个可点击的超链接。**必须主动询问用户该链接的完整URL**（如 QQ 空间链接、个人主页链接等）。收到链接后，在自我介绍条的 `intro_link` 字段中配置；如果是亲友的蓝名直达，则在 `friends_group` 的对应 friend 中填入 `url`。

**Footer 规则：**
footer 只应包含**重要信息**：蓝名直达链接、个人主页/个人简历链接等关键网址，以及一句结束语。**不要**在 footer 中出现次要信息，如"我在用XX和YY音乐软件"、"平时爱喝奶茶"等日常琐碎——这些应放在 friendship 板块的对应 block 中。

**重要：Content内容格式化规则：**

1. 自动识别"重点"：如网站名、重要概念、关键信息，使用 `highlight(关键词)` 或 `highlight-accent(关键词)` 或 `highlight-primary(关键词)`。绝对不要在非 `content`字段内包含 `highlight`或 `addurl`。
2. 自动识别"链接"：所有网址链接自动使用 `addurl(链接文字, 网址链接)` 格式
3. 示例：
   ```
   原文："欢迎访问 world.sch-nie.com，特别注意 2025MOXUE"
   转换后："欢迎访问 addurl(world.sch-nie.com,https://world.sch-nie.com)，特别注意 highlight(2025MOXUE)"
   ```

- footer格式：每个信息单独一行，参考模板 assets/config.json 的格式：
  ```json
  "footer": {
    "blocks": [
      {
        "content": "小故事链接：addurl(world.sch-nie.com,https://world.sch-nie.com)"
      },
      {
        "content": "个人简历：addurl(resume.sch-nie.com,https://resume.sch-nie.com)"
      },
      {
        "content": "总之，欢迎您来和我扩列~"
      }
    ]
  }
  ```

### 第三步：询问缺失信息

必须询问以下字段：

1. **头像图片链接** — 用户提供图片URL，如无则可跳过使用默认占位图
2. **头像描述** — alt 文本
3. **暗号词（secret word）** — 好友添加时的验证关键词，默认可设为用户的 cn + 年份（如"星槐2025"）
4. **配色方案** — 需要 4 个颜色（白天 primary + 白天 accent + 夜间 primary + 夜间 accent）。提供两种选择方式：

**方式一：预设套组（推荐）**
向用户展示以下预设，让用户选择编号：

| 编号 | 套组名称       | 白天 Primary | 白天 Accent | 夜间 Primary | 夜间 Accent |
| ---- | -------------- | ------------ | ----------- | ------------ | ----------- |
| 1    | 海洋蓝（推荐） | `#3b82f6`  | `#fbbf24` | `#8b5cf6`  | `#a855f7` |
| 2    | 森林绿         | `#10b981`  | `#34d399` | `#059669`  | `#6ee7b7` |
| 3    | 日落橙         | `#f97316`  | `#fbbf24` | `#ea580c`  | `#facc15` |
| 4    | 樱花粉         | `#ec4899`  | `#f472b6` | `#be185d`  | `#f9a8d4` |
| 5    | 薰衣草紫       | `#8b5cf6`  | `#c084fc` | `#7c3aed`  | `#e9d5ff` |
| 6    | 深海青         | `#0891b2`  | `#22d3ee` | `#0e7490`  | `#67e8f9` |
| 7    | 暗夜红         | `#dc2626`  | `#f87171` | `#b91c1c`  | `#fca5a5` |
| 8    | 薄荷绿         | `#14b8a6`  | `#2dd4bf` | `#0d9488`  | `#5eead4` |

**方式二：自定义颜色**
如果用户对预设不满意，逐一询问 4 个颜色：

1. 白天主色（day primary）— 页面的主色调
2. 白天强调色（day accent）— 按钮、标签、高亮等
3. 夜间主色（night primary）— 深色背景下的主色，通常比白天更深/饱和度更高
4. 夜间强调色（night accent）— 深色背景下的强调色

如用户只提供 1 个颜色，默认用该颜色作为白天 primary，其余按"海洋蓝"套组的比例自动推算。

### 第四步：生成HTML

运行 `scripts/generate.py` 脚本生成最终HTML，输出到项目根目录下的 `output/output.html`

## 生成脚本使用方法

```bash
python scripts/generate.py -c user_config.json -o output/output.html
```

可选参数：

- `-c` / `--config`：用户配置JSON文件路径（默认 `user_config.json`）
- `-r` / `--reference`：参考配置JSON文件路径（可选，默认 `assets/config.json`）
- `-o` / `--output`：输出HTML文件路径（默认 `output.html`）

带参考配置的用法（用户配置缺失字段时自动从参考配置填充）：

```bash
python scripts/generate.py -c user_config.json -r assets/config.json -o output/output.html
```

## Block 类型

所有板块通过 `blocks` 数组配置，支持以下 9 种 block 类型，可自由组合。

### 1. `content` - 普通内容块

```json
{
  "type": "content",
  "icon": "fa-star",
  "title": "标题",
  "content": "内容文本（支持 highlight 和 addurl 格式）",
  "intro_link": {
    "icon": "fa-file-text-o",
    "title": "链接标题",
    "url": "https://example.com"
  }
}
```

`intro_link` 为可选字段，用于在内容块底部添加一个跳转按钮。

### 2. `divider` - 分割线

```json
{
  "type": "divider",
  "icon": "fa-heart"
}
```

### 3. `personality_group` - 性格特点组（2列网格，点击弹窗）

**适用场景：** 性格特质、MBTI维度、属性标签等与"人本身特质"相关的内容。视觉风格为蓝色主题圆角卡片，点击弹出详细描述。

```json
{
  "type": "personality_group",
  "icon": "fa-star",
  "title": "性格特点",
  "items": [
    {
      "icon": "fa-feather",
      "title": "性格特质1",
      "subtitle": "一句话概括",
      "description": "详细描述（点击弹窗显示）"
    }
  ]
}
```

### 4. `hobby_group` - 兴趣爱好组（2列网格，点击弹窗）

**适用场景：** 游戏、动漫、音乐、运动、创作等"兴趣/爱好"相关内容。视觉风格为蓝色主题标签卡片，点击弹出详细描述。

```json
{
  "type": "hobby_group",
  "icon": "fa-heart",
  "title": "兴趣爱好",
  "items": [
    {
      "icon": "🎮",
      "title": "爱好名称",
      "subtitle": "简要描述（如"养成系二游"、"每天摸鱼画画"），不要填英文名",
      "description": "详细描述（点击弹窗显示）"
    }
  ]
}
```

`subtitle` 是**简短的描述语**（如"养成系二游"、"每天摸鱼画画"），不要填游戏的英文原名（如"Honkai: Star Rail"）。

### 使用区分指南

- 用户提到了 **MBTI、性格词（活泼/社恐/i人/抽象）、星座、价值观** → 用 `personality_group`
- 用户提到了 **游戏、动画、音乐软件、运动项目、绘画/写作等创作爱好** → 用 `hobby_group`
- 用户提到的"推/喜欢的角色"如果数量多，可以单独用一个 `hobby_group`（标题如"喜欢的角色"），放在游戏日常之后

### 5. `red_line_group` - 雷点组（列表，点击划线）

```json
{
  "type": "red_line_group",
  "icon": "fa-times-circle",
  "title": "雷点",
  "items": [
    {
      "icon": "fa-exclamation-triangle",
      "content": "雷点内容（支持 highlight 和 addurl 格式）"
    }
  ]
}
```

### 6. `your_red_line_group` - 可能雷到你的组（列表，点击抖动）

```json
{
  "type": "your_red_line_group",
  "icon": "fa-lightbulb-o",
  "title": "可能雷到你的",
  "items": [
    {
      "icon": "fa-info-circle",
      "content": "内容（支持 highlight 和 addurl 格式）"
    }
  ]
}
```

### 7. `external_link_group` / `link_group` - 外部链接组（2列网格）

```json
{
  "type": "external_link_group",
  "icon": "fa-external-link",
  "title": "外部链接",
  "items": [
    {
      "icon": "fa-globe",
      "title": "链接标题",
      "subtitle": "example.com",
      "url": "https://example.com"
    }
  ]
}
```

`external_link_group` 和 `link_group` 渲染效果相同，可互换使用。`external_link_group` 使用蓝色主题，`link_group` 使用黄/橙色主题。

### 8. `gallery_group` - 图片轮播图

```json
{
  "type": "gallery_group",
  "icon": "fa-picture-o",
  "title": "图片分享",
  "gallery_title": "图片展示集合",
  "slides": [
    {
      "src": "https://example.com/image.jpg",
      "alt": "图片描述",
      "caption": "图片标题"
    }
  ]
}
```

支持多个独立的 gallery 实例，每个有独立的轮播、导航和键盘快捷键。

### 9. `friends_group` - 亲友展示组

```json
{
  "type": "friends_group",
  "icon": "💕",
  "title": "我的亲友们",
  "categories": [
    {
      "category": "好闺蜜",
      "icon": "💖",
      "friends": [
        { "name": "好友A" }
      ]
    },
    {
      "category": "亲友",
      "icon": "🌟",
      "friends": [
        { "name": "好友B", "url": "https://example.com" },
        { "name": "好友C" },
        { "name": "好友D", "url": "https://example.com" }
      ]
    }
  ]
}
```

每个 friend 对象的字段：

- `name`（必填）- 好友名称
- `url`（可选）- 有 url 时标签可点击跳转，无 url 则为纯展示
- `avatar`（可选）- 好友头像图片链接

颜色完全跟随主题色（primary/accent），自动适配白天/夜间模式。

## Content 格式说明

所有 `content` 字段都支持特殊格式：

**高亮文本：**

- `highlight(text)` 或 `highlight-accent(text)` - 强调色（accent）高亮
- `highlight-primary(text)` - 主色调（primary）高亮

**添加链接：**

- `addurl(显示文字, 网址链接)` - 添加可点击链接

## 颜色配置说明

只需设置 4 个基础颜色，所有衍生色由脚本自动计算（含 RGB 值、浅色/深色变体、柔阴影色、渐变色等）。阴影和边框等装饰元素会自动使用主题色的 rgba() 版本，确保全页色彩和谐统一。

**白天模式：**

- `colors.day.primary` - 主色调（如 `#3b82f6`）
- `colors.day.accent` - 强调色（如 `#fbbf24`）

**夜间模式：**

- `colors.night.primary` - 主色调（如 `#8b5cf6`）
- `colors.night.accent` - 强调色（如 `#a855f7`）

脚本会自动生成以下颜色族：

- `_light` / `_lighter` / `_ultralight` — 浅色/极淡变体（用于背景、hover）
- `_dark` — 深色变体（用于硬阴影、边框）
- `_rgb` — RGB 格式（用于 `rgba()` 柔阴影）
- 夜间模式专用深色背景色等

**预设套组速查（8套）：**

| 编号 | 套组名称 | 白天 Primary | 白天 Accent | 夜间 Primary | 夜间 Accent |
| ---- | -------- | ------------ | ----------- | ------------ | ----------- |
| 1    | 海洋蓝   | `#3b82f6`  | `#fbbf24` | `#8b5cf6`  | `#a855f7` |
| 2    | 森林绿   | `#10b981`  | `#34d399` | `#059669`  | `#6ee7b7` |
| 3    | 日落橙   | `#f97316`  | `#fbbf24` | `#ea580c`  | `#facc15` |
| 4    | 樱花粉   | `#ec4899`  | `#f472b6` | `#be185d`  | `#f9a8d4` |
| 5    | 薰衣草紫 | `#8b5cf6`  | `#c084fc` | `#7c3aed`  | `#e9d5ff` |
| 6    | 深海青   | `#0891b2`  | `#22d3ee` | `#0e7490`  | `#67e8f9` |
| 7    | 暗夜红   | `#dc2626`  | `#f87171` | `#b91c1c`  | `#fca5a5` |
| 8    | 薄荷绿   | `#14b8a6`  | `#2dd4bf` | `#0d9488`  | `#5eead4` |

若用户自选颜色，直接将对应值写入 `colors` 配置即可，格式不变。

## 目录（TOC）配置说明

`toc` 定义页面中出现的大板块（卡片）的顺序、标题和图标：

```json
"toc": [
  {
    "id": "overview",
    "title": "概述",
    "icon": "fa-star"
  },
  {
    "id": "friendship",
    "title": "个人扩列条",
    "icon": "fa-heart"
  },
  {
    "id": "personal_media",
    "title": "个人媒体",
    "icon": "fa-picture-o"
  }
]
```

**注意事项：**

- `toc` 中的 `id` 必须与 JSON 根级下的板块配置对象名称一致
- `footer` 和 `important_warning` 是特殊板块，不出现在 toc 中，但始终渲染
- 支持自由添加/删除/重新排列板块
- 图标可混用 Font Awesome（`fa-star`）和 Emoji（`💕`）

## 参考配置

参考 assets/config.json 了解完整的配置结构。
