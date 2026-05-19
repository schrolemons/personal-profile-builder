# 个人扩列条生成器 (Skill)

一键生成个人扩列条HTML页面。用户用自然语言描述自己，自动转换为精美网页。

> 最近更新：2026-05-19 — 配色系统视觉优化、夜间模式全面修复、智能柔阴影系统

## 📦 安装方式

### 方式一：让 Agent 帮你安装（推荐）

直接对 Agent 说：

> "帮我安装 personal-profile-builder skill"

Agent 会自动为你完成安装配置。

### 方式二：Git 方式安装

```bash
# 1. 克隆或下载这个 skill 到你的 skills 目录
cd your-project/.trae/skills
git clone https://github.com/schrolemons/personal-profile-builder.git

# 2. 重启你的 Agent，skill 就会自动加载
```

## 🚀 使用方法

### 快速开始

直接告诉 Agent 你想要什么样的扩列条，例如：

> "帮我生成一个个人扩列条，我叫墨薛，是一只大尾巴、白毛异瞳的黄色小狼，来自虹九宇宙，喜欢鼓捣网站和世界观"

### 使用流程

1. **描述需求** - 用自然语言告诉 Agent 你的信息
2. **补充信息** - Agent 会询问缺失的必要信息（头像、主题色等）
3. **生成页面** - 自动生成精美的 HTML 页面

## 🎯 核心特点

- **📝 简单配置** - 用自然语言描述即可，无需编写代码
- **🎨 智能配色** - 仅需 4 个基础色，自动生成所有衍生色、阴影、渐变
- **🌈 主题柔阴影** - 所有组件阴影自动跟随主题色，色彩和谐统一
- **🌓 双模式完善** - 白天/夜间模式全部组件均有独立适配，切换无死角
- **📱 响应式设计** - 完美适配桌面端和移动端
- **⚡ 丰富交互** - 轮播图、弹窗、动画效果、hover 反馈等
- **🔧 高度灵活** - 支持 9 种 block 类型、自定义板块、TOC 自由排列

## 📁 文件说明

| 文件                        | 说明                                   |
| --------------------------- | -------------------------------------- |
| `scripts/generate.py`     | Python 生成脚本（含完整 CSS 动态生成） |
| `assets/config.json`      | 参考配置模板                           |
| `assets/basic-styles.css` | 基础 CSS 框架样式                      |
| `assets/script.js`        | JavaScript 交互文件                    |
| `README.md`               | 本使用说明文档                         |
| `SKILL.md`                | AI Agent 工作流程说明                  |
| `references/`             | 参考文档（配置规范、格式指南）         |

## 📖 Block 类型

### 各 Block 类型详细格式

#### 1. `content` - 普通内容块

```json
{
  "type": "content",
  "icon": "fa-star",           // 图标（Font Awesome 或 Emoji）
  "title": "标题",            // 块标题
  "content": "内容文本",      // 内容（支持 highlight 和 addurl 格式）
  "intro_link": {             // 可选，底部链接
    "icon": "fa-file-text-o",
    "title": "链接标题",
    "url": "https://example.com"
  }
}
```

#### 2. `divider` - 分割线

```json
{
  "type": "divider",
  "icon": "fa-heart"          // 分割线中间的图标
}
```

#### 3. `personality_group` - 性格特点组

```json
{
  "type": "personality_group",
  "icon": "fa-star",
  "title": "性格特点",
  "items": [
    {
      "icon": "fa-feather",   // 项目图标
      "title": "性格特质1",   // 特质标题
      "subtitle": "简要描述", // 副标题
      "description": "详细描述" // 详细描述（点击弹窗显示）
    }
  ]
}
```

#### 4. `hobby_group` - 兴趣爱好组

```json
{
  "type": "hobby_group",
  "icon": "fa-heart",
  "title": "兴趣爱好",
  "items": [
    {
      "icon": "🎮",           // 项目图标（Emoji 或 Font Awesome）
      "title": "爱好1",       // 爱好标题
      "subtitle": "爱好描述", // 副标题
      "description": "详细描述" // 详细描述（点击弹窗显示）
    }
  ]
}
```

#### 5. `red_line_group` - 雷点组

```json
{
  "type": "red_line_group",
  "icon": "fa-times-circle",
  "title": "雷点",
  "items": [
    {
      "icon": "fa-exclamation-triangle",
      "content": "雷点内容"    // 内容（支持 highlight 和 addurl 格式）
    }
  ]
}
```

#### 6. `your_red_line_group` - 可能雷到你的组

```json
{
  "type": "your_red_line_group",
  "icon": "fa-lightbulb-o",
  "title": "可能雷到你的",
  "items": [
    {
      "icon": "fa-info-circle",
      "content": "内容"        // 内容（支持 highlight 和 addurl 格式）
    }
  ]
}
```

#### 7. `external_link_group` - 外部链接组

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

#### 8. `gallery_group` - 图片轮播图

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

#### 9. `friends_group` - 亲友展示组

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

每个朋友的 `url` 和 `avatar` 均为可选。有 `url` 时可点击跳转，无 `url` 则纯展示。

## ✨ Content 格式说明

所有 content 字段都支持多种特殊格式：

**高亮文本：**

- `highlight(text)` 或 `highlight-accent(text)` - 强调色高亮
- `highlight-primary(text)` - 主色调高亮

**添加链接：**

- `addurl(text, url)` - 添加链接

## 🎨 颜色配置说明

只需设置 4 个基础颜色！

**白天模式（2色）：**

- `colors.day.primary` - 主色调（默认：#3b82f6）
- `colors.day.accent` - 强调色（默认：#fbbf24）

**夜间模式（2色）：**

- `colors.night.primary` - 主色调（默认：#8b5cf6）
- `colors.night.accent` - 强调色（默认：#a855f7）

## 🛠️ 手动使用

如果你想手动运行生成脚本：

```bash
python generate.py -c user_config.json -o output.html
```

## 📚 目录（TOC）配置说明

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

## 🔧 技术要求

- Python 3.x
- 任何现代浏览器

---

**祝你创建自己的扩列条愉快！** 🎉
