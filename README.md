# 个人扩列条模板系统

一个功能强大、易于定制的个人扩列条模板系统，通过简单的 JSON 配置即可创建精美的个人主页。

## 🎯 核心特点

- **📝 简单配置** - 通过 JSON 文件即可完成所有内容和样式的定制，无需编写代码
- **🎨 主题配色** - 支持白天/夜间双模式，仅需配置 4 个基础颜色即可自动生成完整配色方案
- **📱 响应式设计** - 完美适配桌面端和移动端，提供一致的用户体验
- **⚡ 丰富交互** - 包含轮播图、弹窗、动画效果等多种交互功能
- **🔧 高度灵活** - 支持自定义板块、多种内容类型、自由排列组合
- **🧠 LLM集成** - 支持自然语言输入，自动转换为配置格式

## ✨ 功能亮点

- 🎨 **图标自由** - 所有图标支持 Font Awesome 和 Emoji 两种格式
- 🖼️ **多图轮播** - 支持在任意位置添加多个独立的图片轮播图
- ✨ **动态高亮** - 高亮样式自动基于主题色生成，支持主色和强调色两种
- 🔐 **预留彩蛋** - 支持暗号词功能，重要内容仅对"有耐心"的用户显示
- 🛡️ **优雅降级** - 配置缺失时自动使用默认值

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `config.json` | 参考配置文件（提供默认值和完整结构） |
| `generate.py` | Python脚本（运行此脚本来生成最终的 HTML） |
| `basic-styles.css` | CSS样式文件（框架样式和主题定义） |
| `script.js` | JavaScript文件（交互功能） |
| `output.html` | 生成的最终 HTML 文件 |
| `README.md` | 使用说明文档 |
| `MODIFICATIONS.md` | 系统修改记录文档 |

## 使用方法

### 1. 编辑配置文件

创建 `user_config.json` 文件，根据需要修改各项配置。**无需提供所有字段**，缺失字段会自动使用 `config.json` 中的默认值。

### 2. 运行脚本生成 HTML

```bash
python generate.py -c user_config.json -r config.json -o output.html
```

### 3. 查看结果

脚本会生成 `output.html` 文件，你可以用任何浏览器打开查看效果。

## 目录（TOC）配置说明

目录定义网站中出现的大板块（卡片）的列表，包括它们的顺序、标题和图标。

**注意：** `footer` 和 `important_warning` 这两部分是特殊的，不会出现在 toc 中。

### toc 结构

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
    }
]
```

### 添加自定义板块

1. 在 `toc` 中添加新的条目，设置唯一的 `id`
2. 在配置中添加一个与 id 同名的配置对象，包含 blocks 数组

## 配置合并规则

1. **用户配置优先**：用户提供的字段会覆盖参考配置
2. **递归合并**：嵌套对象会递归合并，保留双方的键
3. **列表处理**：用户提供列表则使用用户的，否则使用参考配置
4. **自动生成**：夜间模式颜色会根据白天模式自动计算

## 颜色配置说明

只需设置 4 个基础颜色！

**白天模式（2色）：**
- `colors.day.primary` - 主色调（默认：#3b82f6）
- `colors.day.accent` - 强调色（默认：#fbbf24）

**夜间模式（2色）：**
- `colors.night.primary` - 主色调（默认：#8b5cf6）
- `colors.night.accent` - 强调色（默认：#a855f7）

## 通用配置说明

通过 toc 配置的所有板块都支持任意数量的 blocks。

### block 类型：

- **`type: "content"`** - 普通内容块
- **`type: "divider"`** - 分割线
- **`type: "personality_group"`** - 性格特点组
- **`type: "hobby_group"`** - 兴趣爱好组
- **`type: "red_line_group"`** - 雷点组
- **`type: "your_red_line_group"`** - 可能雷到你的组
- **`type: "external_link_group"`** - 外部链接组
- **`type: "gallery_group"`** - 图片轮播图

## Content 格式说明

所有 content 字段都支持多种特殊格式：

**高亮文本：**
- `highlight(text)` 或 `highlight-accent(text)` - 强调色高亮
- `highlight-primary(text)` - 主色调高亮

**添加链接：**
- `addurl(text, url)` - 添加链接

## CLI 参数

```bash
python generate.py --help
```

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `--config` | `-c` | 用户配置JSON文件路径 | `user_config.json` |
| `--reference` | `-r` | 参考配置JSON文件路径 | `config.json` |
| `--output` | `-o` | 输出HTML文件路径 | `output.html` |

## 注意事项

- 用户无需提供所有字段，缺失字段自动使用参考配置的默认值
- 雷点、可能雷到你的等字段为可选，不提供则不显示对应板块
- 头像链接为空时会使用默认头像生成服务
- 暗号词为空时不会显示重要提示板块
- toc 中的板块 id 需要与配置对象名称一致

## 技术要求

- Python 3.x
- 任何现代浏览器

祝你创建自己的扩列条愉快！
