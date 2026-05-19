# 配置文件结构说明

## 基础结构

```json
{
  "page_title": "页面标题",
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
  ],
  "header": {
    "title": "标题",
    "subtitle": "副标题"
  },
  "avatar": {
    "src": "https://example.com/avatar.jpg",
    "alt": "头像描述"
  },
  "display": {
    "version": "2.0",
    "secret_word": "secret",
    "update_date": "2024"
  },
  "colors": {
    "day": {
      "primary": "#3b82f6",
      "accent": "#fbbf24"
    },
    "night": {
      "primary": "#8b5cf6",
      "accent": "#a855f7"
    }
  }
}
```

## 板块类型

### content
普通内容块

```json
{
  "type": "content",
  "icon": "fa-star",
  "title": "标题",
  "content": "内容文本，支持 addurl(text, url) 和 highlight(text)"
}
```

### personality_group
性格特点网格

```json
{
  "type": "personality_group",
  "icon": "fa-star",
  "title": "性格特点",
  "items": [
    {
      "icon": "fa-feather",
      "title": "活泼",
      "subtitle": "性格描述",
      "description": "详细说明"
    }
  ]
}
```

### hobby_group
兴趣爱好组

```json
{
  "type": "hobby_group",
  "icon": "fa-heart",
  "title": "兴趣爱好",
  "items": [
    {
      "icon": "🎮",
      "title": "游戏",
      "subtitle": "爱好描述",
      "description": "详细说明"
    }
  ]
}
```

### external_link_group
外部链接组

```json
{
  "type": "external_link_group",
  "icon": "fa-external-link",
  "title": "外部链接",
  "items": [
    {
      "icon": "fa-globe",
      "title": "链接标题",
      "subtitle": "网站名称",
      "url": "https://example.com"
    }
  ]
}
```

### gallery_group
图片轮播组

```json
{
  "type": "gallery_group",
  "icon": "fa-picture-o",
  "title": "图片分享",
  "gallery_title": "我的相册",
  "slides": [
    {
      "src": "https://example.com/image.jpg",
      "alt": "图片描述",
      "caption": "图片标题"
    }
  ]
}
```
