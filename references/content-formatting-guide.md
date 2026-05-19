# Content内容格式化指南

## 基本规则

### 1. 链接处理 - addurl()

所有网址链接必须使用 `addurl()` 格式：
```
格式：addurl(显示文字, 网址链接)
示例：addurl(world.sch-nie.com, https://world.sch-nie.com)
```

**识别场景：**
- 完整网址：`https://example.com`
- 域名：`example.com`
- 特定提及的网站名

---

### 2. 高亮处理 - highlight()

重要关键词使用高亮格式：
```
基本高亮：highlight(关键词) 或 highlight-accent(关键词)
主色高亮：highlight-primary(关键词)
```

**识别场景：**
- 网站名称、产品名
- 暗号词、密码词
- 重要概念、关键时间
- 特殊标记、关键词
- 强调的内容

---

## 完整示例

### 示例1：带链接和重点的句子
```
原文：欢迎访问 world.sch-nie.com，暗号是 2025MOXUE
转换后：欢迎访问 addurl(world.sch-nie.com, https://world.sch-nie.com)，暗号是 highlight(2025MOXUE)
```

### 示例2：多个链接
```
原文：访问 worldview 或 resume 了解更多
转换后：访问 addurl(worldview, https://world.sch-nie.com) 或 addurl(resume, https://resume.sch-nie.com) 了解更多
```

### 示例3：重点强调
```
原文：特别注意！绝不可以！
转换后：特别注意！highlight-accent(绝不可以)！
```

---

## 更多示例

### 示例4
```
原文：我的世界观网站是 world.sch-nie.com，简历在 resume.sch-nie.com
转换后：我的世界观网站是 addurl(world.sch-nie.com, https://world.sch-nie.com)，简历在 addurl(resume.sch-nie.com, https://resume.sch-nie.com)
```

### 示例5
```
原文：加好友时请告诉我 2025MOXUE，这是暗号
转换后：加好友时请告诉我 highlight(2025MOXUE)，这是暗号
```

---

## 配色说明

- `highlight()` 和 `highlight-accent()` 使用强调色（黄色）
- `highlight-primary()` 使用主色调（蓝色）
- 夜间模式会自动调整颜色
