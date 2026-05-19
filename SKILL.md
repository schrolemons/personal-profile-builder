---
name: "personal-profile-builder"
description: "一键生成个人扩列条HTML页面。用户用自然语言描述自己，自动转换为精美网页。"
---

# 个人扩列条生成器

## 功能简介

帮助用户快速创建精美的个人扩列条网页。用户用自然语言描述自己，系统自动转换为JSON配置并生成HTML页面。

## 使用流程

1. 用户用自然语言描述扩列条内容
2. 系统分析内容并识别缺失信息
3. 向用户询问缺失的字段（头像、主题色、secret word等）
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
- 只提取用户明确提到的信息，不要编造
- toc包含三个部分：
  - overview（概述，**总结**性格、喜好、扩列需求，用简洁的总结性语言，**不是**直接复制用户原话）
    - 示例：用户说"我是一只大尾巴、白毛异瞳的INTJ-A黄色小狼~来自虹九宇宙。性格平和、抽象、包容性极强，喜欢鼓捣网站和世界观啦～期待与您扩列～"
    - overview应该是简洁的总结，而不是原话复制
  - friendship（个人扩列条，核心内容）
  - personal_media（个人媒体，仅在有链接或图片时添加）
- header包含title和subtitle
- display包含version（默认"2.0"）和update_date（默认当前年份）

**重要：Content内容格式化规则：**
1. 自动识别"重点"：如网站名、重要概念、关键信息，使用 `highlight(关键词)` 或 `highlight-accent(关键词)` 或 `highlight-primary(关键词)`
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
1. 头像图片链接
2. 头像描述
3. 暗号词（secret word）
4. 主色调（十六进制颜色，如 #3b82f6）
5. 强调色（十六进制颜色，如 #fbbf24）

### 第四步：生成HTML

运行 `scripts/generate.py` 脚本生成最终HTML，输出到项目根目录下的 `output/output.html`

## 生成脚本使用方法

```bash
python scripts/generate.py -c user_config.json -o output/output.html
```

## 参考配置

参考 assets/config.json 了解完整的配置结构。
