# 模板系统修改记录

## 2026-05-19 - 配色系统视觉优化、夜间模式全面修复、多组件细节精修

### 修改的文件

1. **generate.py** - CSS 生成逻辑重大优化

   - 新增 `hex_to_rgb()` 辅助函数，用于生成 `rgba()` 颜色值
   - 新增 `day_accent_rgb` / `day_primary_rgb` / `night_accent_rgb` / `night_primary_rgb` 变量
   - 新增 `night_primary_ultralight` / `night_accent_ultralight` 极淡色变量
   - body 背景渐变从硬编码改为跟随用户配色的 `day_accent_ultralight → day_primary_ultralight`
   - `.cute-card` 添加动态渐变背景 + accent 色调柔阴影（日夜双模式）
   - 所有柔阴影从 `rgba(0,0,0,...)` 改为 `rgba(primary/accent_rgb, ...)`，全面跟随主题色
   - 修复 19+ 处多值 `box-shadow` 中无效的多 `!important` 语法（仅保留声明末尾一个）
   - 补充夜间模式缺失的 `dynamic-primary-lighter` / `dynamic-accent-lighter` 规则
   - `.moxue-avatar` 柔阴影升级为 accent 色调
   - `.cute-monitor` 柔阴影升级为 primary 色调（日夜双模式）
   - `.scroll-button` 柔阴影升级为 accent/primary 色调（日夜双模式）
   - `.toc-button` / `.toc-panel` 柔阴影升级为 accent 色调
   - `.paw-icon` / `.info-box` 柔阴影升级为 accent 色调（日夜双模式）
   - 弹窗样式全面升级（`.hobby-modal` / `.personality-modal` / `.confirm-modal`）：
     - 边框从 `border-color` 改为 `border: 4px solid`，视觉更明显
     - header 分隔线改为 `2px dashed`
     - 柔阴影升级为 primary/accent 色调
     - 夜间模式弹窗内容文字色优化（`#cbd5e1` → `#c4b5fd` / `#e0e7ff`）
   - 新增夜间模式 `#lightbox` 背景和边框适配
   - 新增 `highlight-green/purple/orange/pink` 夜间模式样式
   - 新增时间栏 `bg-white/60` 夜间半透明深色背景
   - `.cute-list-item` 从 `border-left-color` 改为 `border-left: 4px solid`
   - `.box-card` hover 添加彩色柔阴影（日夜双模式）
   - `.friend-tag` / `.friend-tag-link` 完整颜色规则（日间+夜间+悬停）
   - `.friend-tag-link:hover` 变为 full accent 背景+白色文字+accent 阴影
   - `.toc-panel` 添加 `background: #ffffff` + `border: 2px solid`
   - 新增 `.toc-title` / `.toc-item` / `.toc-text` 动态颜色规则（日间+夜间 hover/active）
   - `.cute-link` 添加夜间模式颜色和 `::after` 渐变
   - `.section-close` 改为 `border: 2px solid`
   - `.carousel-dot` 夜间 hover 添加背景色
   - `.typing-cursor` 夜间改为 `night_accent`
   - 新增 `@keyframes night-strike-pulse` 夜间雷点脉冲动画
2. **basic-styles.css** - 修复硬编码样式

   - 移除 `.friend-tag-link:hover` 中硬编码的 `color: #ffffff`（导致白底白字不可见）

### 新增功能

- ✅ **智能柔阴影系统** - 所有组件的柔阴影自动使用 primary/accent 色调的 rgba()，颜色和谐统一

  - 白天模式：柔阴影使用 `rgba(day_primary_rgb, ...)` 或 `rgba(day_accent_rgb, ...)`
  - 夜间模式：柔阴影使用 `rgba(night_primary_rgb, ...)` 或 `rgba(night_accent_rgb, ...)`
  - 覆盖组件：`.cute-card` / `.moxue-avatar` / `.cute-monitor` / `.scroll-button` / `.toc-panel` / `.toc-button` / `.paw-icon` / `.info-box` / `.box-card` / `.friend-tag`
- ✅ **body 背景动态化** - 页面整体背景渐变从硬编码改为跟随用户 4 色配色的极淡版本
- ✅ **弹窗视觉增强** - 边框加粗（4px）、虚线分隔线、主题色柔阴影、夜间内容文字优化
- ✅ **TOC 面板视觉增强** - 白色/深色背景 + 2px 实线边框 + hover/active 状态高亮
- ✅ **亲友标签交互增强** - 带链接标签 hover 时变为 full accent 背景+白色文字，视觉反馈明确
- ✅ **夜间模式全面覆盖** - lightbox / highlight-green~pink / 时间栏 / typing-cursor / toc-item / cute-link / section-close / carousel-dot / 雷点脉冲动画 等均完成夜间适配

### Bug 修复

- 🐛 **修复** 夜间模式下 blocks 背景颜色不切换 — 补充 `dynamic-primary-lighter` / `dynamic-accent-lighter` 夜间规则
- 🐛 **修复** `.cute-card` 夜间 box-shadow 不生效 — 移除多值 box-shadow 中无效的多 `!important` 语法
- 🐛 **修复** 亲友链接文字颜色消失 — 移除 basic-styles.css 硬编码白色，改为动态生成
- 🐛 **修复** 19+ 处 CSS 声明因多 `!important` 被浏览器忽略的问题
- 🐛 **修复** TOC 面板边框不明显 — 添加白色背景和完整 border 声明

### 保持不变的功能

所有原有功能完全保持不变：

- 目录 (TOC) 配置和板块自定义
- 颜色配置系统（4 个基础色）
- 所有 9 种 block 类型
- 重要事项系统
- Footer 配置
- 夜间模式切换
- 多 Gallery 支持
- Emoji 图标支持
- 动态 Highlight 样式

## 2025-05-19 - 多 Gallery 支持、Emoji 图标、动态 Highlight 样式、Closing Icon 自定义、修复 Secret Word 渲染

### 修改的文件

1. **config.json** - 更新配置示例

   - 在 overview 中添加了 `closing_icon` 配置项
   - 更新了 highlight 示例，展示多种用法
   - 保持完全向后兼容
2. **generate.py** - 重大更新

   - 新增 `_render_icon()` 辅助函数，同时支持 Font Awesome 图标和 emoji
   - 更新 `_render_section()` 支持 `closing_icon` 配置项
   - 更新 `_render_gallery_group()` 支持多个独立的 gallery 实例
   - 更新 `_render_final_warning()` 支持 emoji 图标
   - 更新 `_render_toc()` 支持 emoji 图标
   - 更新所有 block 类型的渲染函数支持 emoji
   - 优化动态颜色系统，新增 `highlight-primary` 和 `highlight-accent` 样式
   - 修改 `_parse_content()` 支持 `highlight-primary(text)` 和 `highlight-accent(text)`
   - 重构 carousel 相关数据结构，支持 `galleries` 数组
   - 修复了 secret_word 渲染逻辑
3. **script.js** - 更新轮播图系统

   - 重构为支持多个独立的 gallery 实例
   - 新增 `getGalleryData()` 辅助函数
   - 更新所有轮播图相关函数支持 gallery id 参数
   - 键盘快捷键自动识别当前视口中的 gallery

### 新增功能

- ✅ **多 Gallery 支持** - 现在可以在页面的任意位置添加任意数量的 `gallery_group`

  - 每个 gallery 有独立的 id、状态、轮播、导航
  - 自动播放独立控制
  - 键盘快捷键智能识别当前视口中的 gallery
  - 完全独立的轮播状态管理
- ✅ **Emoji 图标支持** - 所有图标配置现在同时支持 Font Awesome 和 emoji

  - Section 标题图标
  - Closing 文本图标
  - Divider 图标
  - Block 组图标和项目图标
  - Toc 侧边栏图标
  - Personality/Hobby/Red Line 等所有项目图标
  - 重要警告图标
  - 支持如 `fa-heart` 或 `💕` 两种写法
- ✅ **动态 Highlight 样式** - 高亮颜色现在完全基于主题色自动生成

  - `highlight(text)` 或 `highlight-accent(text)` - 使用强调色渐变
  - `highlight-primary(text)` - 使用主色调渐变
  - 颜色完全从 config.json 的配色方案自动计算
  - 支持渐变背景，视觉效果更美观
  - 夜间模式有专门的适配
- ✅ **Closing Icon 自定义** - 可以自定义 overview 板块关闭文本两侧的图标

  ```json
  "overview": {
      "closing_text": "期待与您扩列～",
      "closing_icon": "💕"  // 或 fa-heart
  }
  ```
- ✅ **修复 Secret Word 渲染** - 确保 secret_word 在重要提示中正确显示

### 更新的配置说明

#### 图标配置

所有图标配置现在支持两种格式：

```json
// Font Awesome 图标
{
    "icon": "fa-heart"
}

// Emoji 图标
{
    "icon": "💕"
}
```

支持图标的所有位置：

- Toc 中的板块图标
- Content block 的图标
- Divider 的图标
- Personality group 的图标和项目图标
- Hobby group 的图标和项目图标
- Red line group 的图标和项目图标
- Your red line group 的图标和项目图标
- External link group 的图标和项目图标
- Gallery group 的图标
- Important warning 的图标
- Closing icon

#### Highlight 格式

```json
// 默认 accent 颜色高亮
"content": "这里是 highlight(高亮文本)的示例"

// 指定 accent 颜色高亮
"content": "这里是 highlight-accent(高亮文本)的示例"

// 指定 primary 颜色高亮
"content": "这里是 highlight-primary(高亮文本)的示例"
```

#### 多 Gallery 配置

```json
{
    "type": "gallery_group",
    "icon": "fa-picture-o",
    "title": "我的相册",
    "gallery_title": "照片展示",
    "slides": [
        {
            "src": "https://example.com/1.jpg",
            "alt": "图片描述",
            "caption": "图片标题"
        }
    ]
}
```

你可以在任意位置添加任意数量的 gallery_group！

### 保持不变的功能

所有原有功能完全保持不变：

- 目录 (TOC) 配置和板块自定义
- 颜色配置系统（4 个基础色）
- 所有 block 类型
- 重要事项系统
- Footer 配置
- 夜间模式

## 2025-05-18 - 初始版本、修复、最终完善、Block 类型系统、个人媒体完整实现、重要事项支持和目录（TOC）配置

### 创建的文件

1. **config.json** - 配置文件

   - 包含网页元数据配置
   - 颜色方案配置（白天模式 2 色 + 夜间模式 2 色）
   - 头像图片配置
   - 标题和副标题配置
   - 时钟显示开关
   - 版本号和版权信息
   - 暗号词配置
   - 更新日期配置
   - 目录 (toc) 配置，用于定义板块顺序和内容
   - 概述部分配置（支持所有 block 类型）
   - 个人扩列条部分配置（支持所有 block 类型）
   - 个人媒体部分配置（支持所有 block 类型）
   - 重要事项配置（支持所有 block 类型，可选项）
   - 底部链接配置（支持任意数量的 blocks）
2. **generate.py** - Python 生成脚本

   - 加载 JSON 配置
   - 应用配置到原始 HTML
   - 自动生成白天模式颜色变体
   - 自动生成夜间模式颜色变体
   - 支持文本内容替换
   - 生成 output.html
   - 支持 content 格式解析（highlight 和 addurl）
   - 完整的 block 类型渲染系统
   - 支持 toc 目录配置，可自由添加/删除/重新排列板块
   - 支持自定义板块
   - 支持 gallery 图片轮播图配置和 JavaScript 更新
   - 支持重要事项渲染
   - 保护 footer 和重要事项不会被删除
   - 动态生成侧边栏目录 toc-items
   - 动态更新 JavaScript 中的 sections 数组、tocIdMap 和 checkAllClosed 函数
3. **README.md** - 使用说明文档

   - 包含完整的使用说明
   - toc 配置详细说明
   - 所有配置项说明
   - 所有 block 类型说明
4. **MODIFICATIONS.md** - 本文件，记录修改历史

### 修改的文件

5. **basic-styles.css** - CSS 样式文件（框架样式和主题定义）
6. **script.js** - JavaScript 文件（交互功能）

> **注意**：后续更新（2025-05-19）已使系统完全独立，不再依赖 basic.html 模板文件。basic.html 现已成为历史文件，可安全删除。

### 功能实现与修复

- ✅ 网页标题配置
- ✅ 颜色方案配置（最终完善为 4 个基础颜色）
  - 白天模式主色调（蓝色）
  - 白天模式强调色（黄色）
  - 夜间模式主色调（紫色）
  - 夜间模式强调色（浅紫色）
- ✅ 头像图片配置
- ✅ 大标题和副标题配置
- ✅ 时钟显示（预留配置项）
- ✅ 版本号配置
- ✅ POWERED BY 版权信息配置
- ✅ 暗号词配置（重要信息中的 {{secret_word}}）
- ✅ 更新日期配置
- ✅ 底部链接配置（支持任意数量的 blocks）
- ✅ **修复了** 夜间模式颜色被意外替换的问题
- ✅ **修复了** 暗号词匹配字符串（从 MOXUE2025 改为 2025MOXUE）
- ✅ **最终简化并完善了** 颜色配置（从 16 个配置项减少到 4 个基础色）
- ✅ **新增了** 完整的颜色自动计算功能
  - 白天模式：从 2 个基础色生成 12 个变体
  - 夜间模式：从 2 个基础色生成 23 个变体
- ✅ **新增了** Footer Blocks 系统
  - 支持任意数量的内容块
  - 支持 highlight(text) 格式进行文本高亮
  - 支持 addurl(text, url) 格式添加链接
  - 自动交替黄色和蓝色星星图标
- ✅ **完成了** 完整的 Block 类型系统
- ✅ **新增了** 重要事项配置支持
  - 支持任意数量和顺序的 blocks
  - 支持所有 block 类型（content, divider 等）
  - content 中的 {{secret_word}} 自动替换
  - 当 secret_word 为空时，重要事项部分完全不渲染
  - 支持高亮和链接格式
- ✅ **新增了** 目录 (TOC) 配置支持
  - 支持完全自由地定义板块顺序
  - 支持添加任意自定义板块
  - 支持删除任意板块
  - 保护 footer 和重要事项不被删除
  - 自定义板块支持所有 block 类型
  - 完全灵活的系统架构
  - **动态生成侧边栏目录 toc-items**
  - **动态更新 JavaScript 中的 sections 数组**
  - **动态更新 JavaScript 中的 tocIdMap 对象**
  - **动态实现 checkAllClosed 函数逻辑**
  - **删除所有板块时自动显示重要事项（如果存在）**

### 最终颜色配置说明

现在配置颜色非常简单，只需要设置 **4 个基础颜色**！

**白天模式（2 色）：**

- `colors.day.primary` - 主色调（默认：蓝色 #3b82f6）
- `colors.day.accent` - 强调色（默认：黄色 #fbbf24）

**夜间模式（2 色）：**

- `colors.night.primary` - 主色调（默认：紫色 #8b5cf6）
- `colors.night.accent` - 强调色（默认：浅紫色 #a855f7）

脚本会自动生成所有其他颜色变体，包括：

- 浅色/深色变体（用于背景、边框、阴影）
- 适合的文字颜色
- RGB 格式颜色值
- 夜间模式专用的深色背景色等

### 完整的目录（TOC）和 Block 类型系统说明

#### 目录（TOC）配置

目录是用于定义网站中出现的大板块（卡片）的列表，包括它们的顺序、标题和图标。你可以完全自由地添加、删除或重新排列这些板块。

**注意：** `footer` 和 `重要事项` 这两部分是特殊的，不会出现在 toc 中，也不能被删除。

**TOC 结构：**

```json
"toc": [
    {
        "id": "overview",
        "title": "概述",
        "icon": "fa-star"  // 或 emoji
    },
    {
        "id": "friendship",
        "title": "个人扩列条",
        "icon": "fa-heart"  // 或 emoji
    }
]
```

**添加自定义板块：**

1. 在 `toc` 中添加新的条目，设置唯一的 `id`
2. 在 config.json 的根级添加一个与 id 同名的配置对象，包含 blocks 数组
3. 在 blocks 数组中添加任意类型的 blocks

#### 通用的 block 类型：

- **`type: "content"`** - 普通内容块（默认类型）

  - `icon` - Font Awesome 图标类名或 emoji
  - `title` - 大标题
  - `content` - 内容文本（支持 highlight 和 addurl 格式）
  - `intro_link` (可选) - 简介链接
- **`type: "divider"`** - 分割线

  - `icon` - 分割线中心的图标（默认 fa-heart）

#### 高级 block 类型：

- **`type: "personality_group"`** - 性格特点组（2列网格，弹窗）
- **`type: "hobby_group"`** - 兴趣爱好组（2列网格，弹窗）
- **`type: "red_line_group"`** - 雷点组（列表，点击划线）
- **`type: "your_red_line_group"`** - 可能雷到你的组（列表，点击抖动）
- **`type: "external_link_group"`** - 外部链接组（2列网格）
- **`type: "gallery_group"`** - 图片轮播图（轮播图组件）
- **`type: "link_group"`** - 链接组（2列网格）

所有 block 类型支持在任意通过 toc 定义的板块中自由使用！

### Content 格式说明（通用）

content 字段支持多种特殊格式：

- **`highlight(text)`** 或 **`highlight-accent(text)`** - 强调色高亮显示文本
- **`highlight-primary(text)`** - 主色调高亮显示文本
- **`addurl(text, url)`** - 添加链接

你可以在 blocks 数组中添加任意数量的内容块！
