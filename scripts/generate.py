#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
灵活的 HTML 生成器 - 使用框架类系统
支持通过 JSON 配置灵活定义各种组件
支持部分字段缺失，自动使用参考配置的默认值
"""

import json
import re
from pathlib import Path


class HTMLGenerator:
    def __init__(self, css_path, js_path, config_path, reference_path=None):
        self.css_content = self._load_file(css_path)
        self.js_content = self._load_file(js_path)
        
        # 加载用户配置
        self.user_config = self._load_json(config_path)
        
        # 加载参考配置（用于填充缺失字段）
        if reference_path and Path(reference_path).exists():
            self.reference_config = self._load_json(reference_path)
        else:
            self.reference_config = {}
        
        # 合并配置：用户配置优先，缺失字段使用参考配置
        self.config = self._merge_configs(self.user_config, self.reference_config)
        
        self.galleries_data = []
        self.secret_word = self.config.get('display', {}).get('secret_word', '')

    def _load_file(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _load_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _merge_configs(self, user, reference):
        """递归合并配置，用户配置优先"""
        if isinstance(user, dict) and isinstance(reference, dict):
            result = reference.copy()
            for key, value in user.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._merge_configs(value, result[key])
                else:
                    result[key] = value
            return result
        elif isinstance(user, list) and isinstance(reference, list):
            # 如果用户提供了列表，使用用户的；否则使用参考的
            return user if user else reference
        else:
            return user if user is not None else reference

    def _render_icon(self, icon):
        if icon.startswith('fa-'):
            return f'<i class="fa {icon}"></i>'
        else:
            return icon

    def _parse_content(self, content):
        result = content
        
        # 处理 addurl(文本,链接)
        addurl_pattern = r'addurl\(([^,]+),\s*([^)]+)\)'
        result = re.sub(addurl_pattern, lambda m: f'<a href="{m.group(2).strip()}" target="_blank" class="cute-link font-semibold">{m.group(1).strip()}</a>', result)
        
        # 处理 highlight-primary(文本)
        highlight_primary_pattern = r'highlight-primary\(([^)]+)\)'
        result = re.sub(highlight_primary_pattern, lambda m: f'<span class="highlight-primary">{m.group(1).strip()}</span>', result)
        
        # 处理 highlight-accent(文本)
        highlight_accent_pattern = r'highlight-accent\(([^)]+)\)'
        result = re.sub(highlight_accent_pattern, lambda m: f'<span class="highlight-accent">{m.group(1).strip()}</span>', result)
        
        # 处理 highlight(文本) - 默认使用 accent 颜色
        highlight_pattern = r'highlight\(([^)]+)\)'
        result = re.sub(highlight_pattern, lambda m: f'<span class="highlight-accent">{m.group(1).strip()}</span>', result)
        
        return result

    def _render_section(self, section_id, section_config):
        title = section_config.get('title', '')
        icon = section_config.get('icon', 'fa-star')
        blocks = section_config.get('blocks', [])
        closing_text = section_config.get('closing_text', '')
        closing_icon = section_config.get('closing_icon', 'fa-heart')
        update_tag = section_config.get('updateTag', False)
        update_date = self.config.get('display', {}).get('update_date', '0000')
        blocks_html = ''
        
        for block in blocks:
            block_type = block.get('type', 'content')
            if block_type == 'divider':
                blocks_html += self._render_divider(block)
            elif block_type in ['personality_group', 'hobby_group', 'red_line_group', 'your_red_line_group']:
                blocks_html += self._render_special_group(block)
            elif block_type in ['external_link_group', 'link_group']:
                blocks_html += self._render_link_group(block)
            elif block_type in ['gallery_group']:
                blocks_html += self._render_gallery_group(block)
            elif block_type in ['content']:
                blocks_html += self._render_content_block(block)
        
        closing_html = ''
        if closing_text:
            closing_icon_rendered = self._render_icon(closing_icon)
            if closing_icon.startswith('fa-'):
                closing_icon_rendered = closing_icon_rendered.replace('"><i', ' text-yellow-400"><i')
                closing_icon_rendered = closing_icon_rendered.replace('i>', 'i text-yellow-400">')
            closing_html = f'''
                <div class="text-center py-6">
                    <p class="text-2xl font-bold text-blue-700">
                        {closing_icon_rendered}
                        {closing_text}
                        {closing_icon_rendered}
                    </p>
                </div>
            '''
        
        update_tag_html = ''
        if update_tag:
            update_tag_html = f'<span class="cute-tag ml-auto"><i class="fa fa-clock-o"></i> update: {update_date}</span>'
        
        title_icon_rendered = self._render_icon(icon)
        return f'''
            <section id="{section_id}-section" class="cute-card p-8 bounce-in closable-section">
                <button class="section-close" onclick="closeSection('{section_id}-section')">✕</button>
                <div class="flex items-center mb-8 title-with-close">
                    <span class="cute-section-title mr-4">
                        {title_icon_rendered}{' ' if icon.startswith('fa-') else '&nbsp;'}{title}
                    </span>
                    {update_tag_html}
                </div>
                <div class="space-y-6">
                    {blocks_html}
                    {closing_html}
                </div>
            </section>
        '''

    def _render_divider(self, block):
        icon = block.get('icon', 'fa-heart')
        icon_rendered = self._render_icon(icon)
        return f'''
            <div class="cute-divider">
                {icon_rendered}
            </div>
        '''

    def _render_special_group(self, block):
        block_type = block.get('type', '')
        icon = block.get('icon', 'fa-star')
        title = block.get('title', '')
        items = block.get('items', [])
        elements_html = ''
        
        icon_rendered = self._render_icon(icon)
        if icon.startswith('fa-'):
            icon_container = f'<span class="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center mr-3 text-white">{icon_rendered}</span>'
        else:
            icon_container = f'<span class="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center mr-3 text-white text-lg">{icon_rendered}</span>'
        
        if block_type == 'personality_group':
            elements_html += f'<div class="bg-gradient-to-r from-blue-50 to-blue-100 rounded-2xl p-6 border-2 border-blue-300"><h3 class="font-bold text-blue-700 text-xl mb-4 flex items-center">{icon_container}{title}</h3>'
            elements_html += self._render_personality_grid(items)
            elements_html += '</div>'
        elif block_type == 'hobby_group':
            elements_html += f'<div class="bg-gradient-to-r from-blue-50 to-blue-100 rounded-2xl p-6 border-2 border-blue-300"><h3 class="font-bold text-blue-700 text-xl mb-4 flex items-center">{icon_container}{title}</h3><div class="grid grid-cols-1 md:grid-cols-2 gap-4">'
            for item in items:
                item_icon = item.get('icon', 'fa-star')
                item_title = item.get('title', '')
                item_subtitle = item.get('subtitle', '')
                item_desc = item.get('description', '')
                escaped_desc = item_desc.replace("'", "\\'").replace('"', '\\"')
                elements_html += f'''<div class="flex items-center gap-4 p-4 bg-white rounded-xl border-2 border-blue-200 hover:border-blue-400 transition-all bounce-scale-item cursor-pointer" onclick="openHobbyModal('{item_title}', '{item_icon}', '{escaped_desc}')">
                    <span class="cute-tag shrink-0">{item_title}</span>
                    <span class="text-slate-700">{item_subtitle}</span>
                </div>'''
            elements_html += '</div></div>'
        elif block_type == 'red_line_group':
            if not items:
                return ''
            elements_html += f'<div class="bg-gradient-to-r from-blue-50 to-blue-100 rounded-2xl p-6 border-2 border-blue-300"><h3 class="font-bold text-blue-700 text-xl mb-4 flex items-center">{icon_container}{title}</h3><ol class="space-y-3">'
            for item in items:
                item_icon = item.get('icon', 'fa-exclamation-triangle')
                item_icon_rendered = self._render_icon(item_icon)
                if item_icon.startswith('fa-'):
                    item_icon_rendered = item_icon_rendered.replace('"><i', ' text-yellow-500 mr-3"><i')
                else:
                    item_icon_rendered = f'<span class="mr-3">{item_icon_rendered}</span>'
                item_content = self._parse_content(item.get('content', ''))
                elements_html += f'''<li class="cute-list-item text-slate-700 red-strike-item" onclick="this.classList.toggle('active')">
                    {item_icon_rendered}
                    <span class="red-strike-text">{item_content}</span>
                </li>'''
            elements_html += '</ol></div>'
        elif block_type == 'your_red_line_group':
            if not items:
                return ''
            elements_html += f'<div class="bg-gradient-to-r from-blue-50 to-blue-100 rounded-2xl p-6 border-2 border-blue-300"><h3 class="font-bold text-blue-700 text-xl mb-4 flex items-center">{icon_container}{title}</h3><ol class="space-y-3">'
            for item in items:
                item_icon = item.get('icon', 'fa-info-circle')
                item_icon_rendered = self._render_icon(item_icon)
                if item_icon.startswith('fa-'):
                    item_icon_rendered = item_icon_rendered.replace('"><i', ' text-yellow-500 mr-3"><i')
                else:
                    item_icon_rendered = f'<span class="mr-3">{item_icon_rendered}</span>'
                item_content = self._parse_content(item.get('content', ''))
                elements_html += f'''<li class="cute-list-item text-slate-700 shake-scale-item">
                    {item_icon_rendered}
                    {item_content}
                </li>'''
            elements_html += '</ol></div>'
            
        return elements_html

    def _render_personality_grid(self, items):
        if not items:
            return ''
        grid_html = '<div class="grid grid-cols-2 gap-4 mt-4">'
        for item in items:
            item_title = item.get('title', '')
            item_icon = item.get('icon', 'fa-star')
            item_subtitle = item.get('subtitle', '')
            item_desc = item.get('description', '')
            escaped_desc = item_desc.replace("'", "\\'").replace('"', '\\"')
            item_icon_rendered = self._render_icon(item_icon)
            if not item_icon.startswith('fa-'):
                item_icon_rendered = f'<span class="text-xl">{item_icon_rendered}</span>'
            grid_html += f'''<div class="bg-white rounded-xl p-4 border-2 border-blue-200 hover:border-blue-400 transition-all cursor-pointer bounce-scale-item" onclick='openPersonalityModal("{item_title}", "{item_icon}", "{escaped_desc}")'>
                <div class="w-12 h-12 bg-gradient-to-br from-blue-400 to-blue-600 rounded-xl flex items-center justify-center mx-auto mb-3 text-white">
                    {item_icon_rendered}
                </div>
                <h4 class="font-bold text-blue-700 mb-1 text-center">{item_title}</h4>
                <p class="text-sm text-slate-600 text-center">{item_subtitle}</p>
            </div>'''
        grid_html += '</div>'
        return grid_html

    def _render_content_block(self, block):
        icon = block.get('icon', 'fa-star')
        title = block.get('title', '')
        content = block.get('content', '')
        intro_link = block.get('intro_link', None)
        link_html = ''
        
        icon_rendered = self._render_icon(icon)
        if icon.startswith('fa-'):
            icon_container = f'<span class="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center mr-3 text-white">{icon_rendered}</span>'
        else:
            icon_container = f'<span class="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center mr-3 text-white text-lg">{icon_rendered}</span>'
        
        if intro_link:
            intro_link_icon = intro_link.get('icon', 'fa-star')
            intro_link_icon_rendered = self._render_icon(intro_link_icon)
            link_html = f'''<a href="{intro_link.get('url', '#')}" target="_blank" class="inline-flex items-center mt-4 cute-link font-semibold bg-white px-4 py-2 rounded-full border-2 border-blue-200 hover:border-blue-400">
                {intro_link_icon_rendered}{' ' if intro_link_icon.startswith('fa-') else '&nbsp;'}{intro_link.get('title', '')}
            </a>'''
        
        return f'''<div class="bg-gradient-to-r from-blue-50 to-blue-100 rounded-2xl p-6 border-2 border-blue-300">
            <h3 class="font-bold text-blue-700 text-xl mb-4 flex items-center">
                {icon_container}
                {title}
            </h3>
            <p class="text-slate-700 leading-relaxed">{self._parse_content(content)}</p>
            {link_html}
        </div>'''

    def _render_link_group(self, block):
        icon = block.get('icon', 'fa-star')
        title = block.get('title', '')
        items = block.get('items', [])
        
        if not items:
            return ''
        
        links_html = ''
        icon_rendered = self._render_icon(icon)
        if icon.startswith('fa-'):
            icon_container = f'<span class="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center mr-3 text-white">{icon_rendered}</span>'
        else:
            icon_container = f'<span class="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center mr-3 text-white text-lg">{icon_rendered}</span>'
        
        for item in items:
            item_icon = item.get('icon', 'fa-star')
            item_icon_rendered = self._render_icon(item_icon)
            if not item_icon.startswith('fa-'):
                item_icon_rendered = f'<span class="text-xl">{item_icon_rendered}</span>'
            links_html += f'''<a href="{item.get('url', '#')}" target="_blank" class="bg-gradient-to-r from-yellow-100 to-orange-100 hover:from-yellow-200 hover:to-orange-200 p-6 rounded-2xl border-3 border-yellow-300 transition-all hover:-translate-y-1 group">
                <div class="flex items-center">
                    <div class="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-400 rounded-xl flex items-center justify-center mr-4 text-white group-hover:scale-110 transition-transform">
                        {item_icon_rendered}
                    </div>
                    <div>
                        <h4 class="font-bold text-yellow-800">{item.get('title', '')}</h4>
                        <p class="text-sm text-slate-600">{item.get('subtitle', '')}</p>
                    </div>
                    <i class="fa fa-arrow-right ml-auto text-yellow-500 group-hover:translate-x-1 transition-transform"></i>
                </div>
            </a>'''
        
        return f'''<div class="bg-gradient-to-r from-yellow-50 to-orange-100 rounded-2xl p-6 border-2 border-yellow-300">
            <h3 class="font-bold text-yellow-800 text-xl mb-4 flex items-center">
                {icon_container}
                {title}
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                {links_html}
            </div>
        </div>'''

    def _render_gallery_group(self, block):
        icon = block.get('icon', 'fa-star')
        title = block.get('title', '')
        gallery_title = block.get('gallery_title', '')
        slides = block.get('slides', [])
        
        if not slides:
            return ''
        
        gallery_id = f'gallery-{len(self.galleries_data)}'
        self.galleries_data.append({
            'id': gallery_id,
            'slides': slides
        })
        
        icon_rendered = self._render_icon(icon)
        if icon.startswith('fa-'):
            icon_container = f'<span class="w-8 h-8 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-full flex items-center justify-center mr-3 text-white">{icon_rendered}</span>'
        else:
            icon_container = f'<span class="w-8 h-8 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-full flex items-center justify-center mr-3 text-white text-lg">{icon_rendered}</span>'
        
        dots_html = ''
        for i, _ in enumerate(slides):
            active_class = ' active' if i == 0 else ''
            dots_html += f'<button onclick="goToSlide(\'{gallery_id}\', {i})" class="carousel-dot{active_class}" data-index="{i}" data-gallery="{gallery_id}"></button>'
        
        first_slide = slides[0] if slides else {}
        monitor_html = f'''<div class="cute-monitor mt-4" data-gallery="{gallery_id}">
            <div class="monitor-header">
                <div class="monitor-dot red"></div>
                <div class="monitor-dot yellow"></div>
                <div class="monitor-dot green"></div>
                <span class="ml-auto text-white font-bold text-sm">
                    <i class="fa fa-folder-open mr-1"></i>{gallery_title}
                </span>
            </div>
            <div class="monitor-content">
                <img id="{gallery_id}-carousel-img" src="{first_slide.get('src', '')}" alt="{first_slide.get('alt', '')}" class="w-full h-64 md:h-80 object-contain rounded-lg cursor-zoom-in" onclick="openLightbox(this.src, this.alt)">
                <div id="{gallery_id}-carousel-caption" class="absolute bottom-4 left-1/2 -translate-x-1/2 bg-white/90 px-4 py-2 rounded-full border-2 border-blue-300 font-bold text-blue-700">
                    {first_slide.get('caption', '')}
                </div>
                <button onclick="prevSlide(\'{gallery_id}\')" class="cute-nav-btn absolute left-4 top-1/2 -translate-y-1/2">
                    <i class="fa fa-chevron-left"></i>
                </button>
                <button onclick="nextSlide(\'{gallery_id}\')" class="cute-nav-btn absolute right-4 top-1/2 -translate-y-1/2">
                    <i class="fa fa-chevron-right"></i>
                </button>
            </div>
            <div class="monitor-footer">
                <div class="flex items-center gap-2">
                    <i class="fa fa-camera text-yellow-500"></i>
                    <span class="font-bold text-blue-700" id="{gallery_id}-feed-counter">001/{str(len(slides)).zfill(3)}</span>
                </div>
                <div class="flex gap-2">{dots_html}</div>
            </div>
        </div>'''
        
        return f'''<div class="bg-gradient-to-r from-green-50 to-blue-50 rounded-2xl p-6 border-2 border-blue-300">
            <h3 class="font-bold text-blue-700 text-xl mb-4 flex items-center">
                {icon_container}
                {title}
            </h3>
            {monitor_html}
        </div>'''

    def _render_final_warning(self):
        warning_config = self.config.get('important_warning', {})
        if not warning_config:
            return ''
        
        blocks = warning_config.get('blocks', [])
        if not blocks:
            return ''
        
        block = blocks[0]
        icon = block.get('icon', 'fa-info-circle')
        title = block.get('title', '')
        content = block.get('content', '').replace('{{secret_word}}', f'<span class="highlight-yellow">{self.secret_word}</span>')
        icon_rendered = self._render_icon(icon)
        
        if not icon.startswith('fa-'):
            icon_rendered = f'<span class="text-xl">{icon_rendered}</span>'
        
        return f'''<section id="final-warning" class="info-box final-warning">
            <div class="flex items-start">
                <div class="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-400 rounded-xl flex items-center justify-center mr-4 text-white floating-star">
                    {icon_rendered}
                </div>
                <div class="flex-1">
                    <h3 class="text-xl font-bold text-yellow-800 mb-3">{title}</h3>
                    <p class="text-yellow-900">
                        <span id="typing-content"></span>
                        <span class="typing-cursor"></span>
                    </p>
                </div>
            </div>
        </section>'''

    def _render_footer(self):
        footer_config = self.config.get('footer', {})
        blocks = footer_config.get('blocks', [])
        links_html = ''
        
        for block in blocks:
            content = block.get('content', '')
            links_html += f'''<p class="text-slate-700 mb-2">
                <i class="fa fa-star text-yellow-400"></i> {self._parse_content(content)}
            </p>'''
        
        display = self.config.get('display', {})
        version = display.get('version', '2.0')
        powered_by = display.get('powered_by', '')
        
        return f'''<footer class="text-center mt-12 pb-8">
            <div class="cute-divider"><i class="fa fa-link"></i></div>
            {links_html}
            <div class="mt-6 pt-6 border-t-2 border-dashed border-yellow-300">
                <p class="text-slate-600 text-sm font-mono">
                    <i class="fa fa-heart text-pink-400"></i>
                    SYSTEM VERSION {version} · POWERED BY {powered_by}
                    <i class="fa fa-heart text-yellow-400"></i>
                </p>
            </div>
        </footer>'''

    def _render_toc(self):
        toc_items = self.config.get('toc', [])
        toc_html = ''
        
        for item in toc_items:
            item_id = item.get('id', '')
            item_title = item.get('title', '')
            item_icon = item.get('icon', 'fa-star')
            icon_rendered = self._render_icon(item_icon)
            toc_html += f'''<div class="toc-item" id="toc-{item_id}" onclick="scrollToSection('{item_id}-section')">
                <span class="toc-icon">{icon_rendered}</span>
                <span class="toc-text">{item_title}</span>
            </div>'''
        
        return toc_html

    def _render_modals(self):
        return '''<div id="hobby-modal" class="hobby-modal-overlay" onclick="closeHobbyModal(event)">
                <div class="hobby-modal" onclick="event.stopPropagation()">
                    <div class="hobby-modal-header">
                        <div class="hobby-modal-title">
                            <div class="hobby-modal-title-icon" id="hobby-modal-icon">🎮</div>
                            <span id="hobby-modal-title">Playing</span>
                        </div>
                        <div class="hobby-modal-close" onclick="closeHobbyModal(event)">✕</div>
                    </div>
                    <div class="hobby-modal-content" id="hobby-modal-content">
                        <p></p>
                    </div>
                </div>
            </div>
            <div id="personality-modal" class="personality-modal-overlay" onclick="closePersonalityModal(event)">
                <div class="personality-modal" onclick="event.stopPropagation()">
                    <div class="personality-modal-header">
                        <div class="personality-modal-title">
                            <div class="personality-modal-title-icon" id="personality-modal-icon">
                                <i class="fa fa-feather"></i>
                            </div>
                            <span id="personality-modal-title">性格</span>
                        </div>
                        <div class="personality-modal-close" onclick="closePersonalityModal(event)">✕</div>
                    </div>
                    <div class="personality-modal-content" id="personality-modal-content">
                        <p></p>
                    </div>
                </div>
            </div>
            <div id="lightbox" class="fixed inset-0 bg-yellow-100/95 z-50 hidden items-center justify-center p-4" onclick="closeLightbox()">
                <div class="relative max-w-4xl max-h-full">
                    <button onclick="closeLightbox()" class="absolute -top-14 right-0 text-yellow-600 hover:text-yellow-800 transition-all text-3xl bg-white rounded-full w-12 h-12 flex items-center justify-center border-3 border-yellow-400 shadow-lg">
                        <i class="fa fa-times"></i>
                    </button>
                    <div class="bg-white rounded-3xl p-4 border-4 border-yellow-300 shadow-2xl">
                        <img id="lightbox-img" src="" alt="" class="max-w-full max-h-[70vh] object-contain rounded-2xl">
                        <p id="lightbox-caption" class="text-center text-yellow-700 mt-4 font-bold text-lg"></p>
                    </div>
                </div>
            </div>
            <div id="confirm-modal" class="confirm-modal-overlay" onclick="closeConfirmModal(event)">
                <div class="confirm-modal" onclick="event.stopPropagation()">
                    <h3>您确定要关闭吗！！</h3>
                    <div class="confirm-modal-buttons">
                        <button class="confirm-btn confirm-btn-yes" onclick="confirmCloseSummary()">确定</button>
                        <button class="confirm-btn confirm-btn-no" onclick="closeConfirmModal()">取消</button>
                    </div>
                </div>
            </div>'''

    def _generate_javascript(self):
        toc_items = self.config.get('toc', [])
        section_ids = [f'{item.get("id")}-section' for item in toc_items]
        toc_map = {}
        for item in toc_items:
            toc_map[f'{item.get("id")}-section'] = f'toc-{item.get("id")}'
        
        warning_config = self.config.get('important_warning', {})
        blocks = warning_config.get('blocks', [])
        warning_content = blocks[0].get('content', '') if blocks else ''
        
        config_js = {
            'sectionIds': section_ids,
            'tocMap': toc_map,
            'galleries': self.galleries_data,
            'secretWord': self.secret_word,
            'warningContent': warning_content
        }
        config_json = json.dumps(config_js, ensure_ascii=False)
        
        return f'''<script>
                window.__config = {config_json};
            </script>
            <script>{self.js_content}</script>'''

    def generate(self, output_path):
        header = self.config.get('header', {})
        avatar = self.config.get('avatar', {})
        sections_html = ''
        
        colors = self.config.get('colors', {})
        day_colors = colors.get('day', {})
        night_colors = colors.get('night', {})
        
        day_primary = day_colors.get('primary', '#3b82f6')
        day_accent = day_colors.get('accent', '#fbbf24')
        night_primary = night_colors.get('primary', '#8b5cf6')
        night_accent = night_colors.get('accent', '#a855f7')
        
        def lighten_color(color, amount=20):
            color = color.lstrip('#')
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            
            r = min(255, r + amount)
            g = min(255, g + amount)
            b = min(255, b + amount)
            
            return f'#{r:02x}{g:02x}{b:02x}'
        
        def darken_color(color, amount=20):
            color = color.lstrip('#')
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            
            r = max(0, r - amount)
            g = max(0, g - amount)
            b = max(0, b - amount)
            
            return f'#{r:02x}{g:02x}{b:02x}'
        
        day_primary_light = lighten_color(day_primary, 50)
        day_primary_lighter = lighten_color(day_primary, 85)
        day_primary_ultralight = lighten_color(day_primary, 88)
        day_primary_dark = darken_color(day_primary, 30)
        day_accent_light = lighten_color(day_accent, 50)
        day_accent_lighter = lighten_color(day_accent, 85)
        day_accent_ultralight = lighten_color(day_accent, 88)
        day_accent_dark = darken_color(day_accent, 30)
        
        night_primary_light = lighten_color(night_primary, 30)
        night_primary_dark = darken_color(night_primary, 20)
        night_accent_light = lighten_color(night_accent, 30)
        night_accent_dark = darken_color(night_accent, 20)
        
        # 只渲染toc中定义的且存在配置的板块
        for item in self.config.get('toc', []):
            section_id = item.get('id')
            if section_id in self.config:
                section_config = self.config[section_id]
                section_config['title'] = item.get('title')
                section_config['icon'] = item.get('icon')
                if section_id == 'personal_media':
                    section_config['updateTag'] = False
                if section_id == 'friendship':
                    section_config['updateTag'] = True
                sections_html += self._render_section(section_id, section_config)
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config.get('page_title', '个人扩列条')}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&family=Noto+Sans+SC:wght@400;500;700" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <style>
        {self.css_content}
        
        body {{
            background: linear-gradient(135deg, #fef3c7 0%, #dbeafe 50%, #fef3c7 100%);
        }}
        
        body.night-mode {{
            background: #0f0f23;
        }}
        
        .dynamic-primary {{ background: {day_primary}; }}
        .dynamic-primary-light {{ background: {day_primary_light}; }}
        .dynamic-primary-lighter {{ background: {day_primary_lighter}; }}
        .dynamic-primary-dark {{ background: {day_primary_dark}; }}
        .dynamic-primary-border {{ border-color: {day_primary}; }}
        .dynamic-primary-text {{ color: {day_primary}; }}
        .dynamic-primary-shadow {{ box-shadow: 0 8px 0 {day_primary_dark}; }}
        
        .dynamic-accent {{ background: {day_accent}; }}
        .dynamic-accent-light {{ background: {day_accent_light}; }}
        .dynamic-accent-lighter {{ background: {day_accent_lighter}; }}
        .dynamic-accent-dark {{ background: {day_accent_dark}; }}
        .dynamic-accent-border {{ border-color: {day_accent}; }}
        .dynamic-accent-text {{ color: {day_accent}; }}
        .dynamic-accent-shadow {{ box-shadow: 0 8px 0 {day_accent_dark}; }}
        
        .dynamic-bg-primary-gradient {{
            background: linear-gradient(145deg, #ffffff 0%, {day_primary_lighter} 100%);
        }}
        .dynamic-bg-accent-gradient {{
            background: linear-gradient(145deg, #ffffff 0%, {day_accent_lighter} 100%);
        }}
        .dynamic-bg-mixed-gradient {{
            background: linear-gradient(135deg, {day_accent_lighter} 0%, {day_primary_lighter} 100%);
        }}
        
        .highlight-primary {{
            background: linear-gradient(120deg, {day_primary_lighter} 0%, {day_primary_light} 100%);
            padding: 2px 6px;
            border-radius: 6px;
            color: #1e3a5f;
            font-weight: 600;
        }}
        
        .highlight-accent {{
            background: linear-gradient(120deg, {day_accent_lighter} 0%, {day_accent_light} 100%);
            padding: 2px 6px;
            border-radius: 6px;
            color: #473403;
            font-weight: 600;
        }}
        
        body.night-mode .dynamic-primary {{ background: {night_primary}; }}
        body.night-mode .dynamic-primary-light {{ background: {night_primary_light}; }}
        body.night-mode .dynamic-primary-dark {{ background: {night_primary_dark}; }}
        body.night-mode .dynamic-primary-border {{ border-color: {night_primary}; }}
        body.night-mode .dynamic-primary-text {{ color: {night_primary}; }}
        body.night-mode .dynamic-primary-shadow {{ box-shadow: 0 8px 0 {night_primary_dark}; }}
        
        body.night-mode .dynamic-accent {{ background: {night_accent}; }}
        body.night-mode .dynamic-accent-light {{ background: {night_accent_light}; }}
        body.night-mode .dynamic-accent-dark {{ background: {night_accent_dark}; }}
        body.night-mode .dynamic-accent-border {{ border-color: {night_accent}; }}
        body.night-mode .dynamic-accent-text {{ color: {night_accent}; }}
        body.night-mode .dynamic-accent-shadow {{ box-shadow: 0 8px 0 {night_accent_dark}; }}
        
        body.night-mode .dynamic-bg-primary-gradient {{
            background: linear-gradient(145deg, #1e1e3f 0%, #2a2a4a 100%);
        }}
        body.night-mode .dynamic-bg-accent-gradient {{
            background: linear-gradient(145deg, #1e1e3f 0%, #2a2a4a 100%);
        }}
        body.night-mode .dynamic-bg-mixed-gradient {{
            background: linear-gradient(135deg, #2a2a4a 0%, #3d3d6a 100%);
        }}
        
        body.night-mode .highlight-primary {{
            background: linear-gradient(120deg, #4c1d95 0%, #7c3aed 100%) !important;
            color: #e0e7ff !important;
        }}
        
        body.night-mode .highlight-accent {{
            background: linear-gradient(120deg, #4c1d95 0%, #7c3aed 100%) !important;
            color: #e0e7ff !important;
        }}
    </style>
</head>
<body class="text-slate-800">
    <div class="sparkle-bg" id="sparkle-bg"></div>
    
    <div class="max-w-5xl mx-auto px-4 py-12 relative z-10">
        <header class="text-center mb-12 bounce-in">
            <div class="inline-flex items-center justify-center mb-8 relative">
                <div id="avatar-container" class="moxue-avatar" onclick="spinAvatar()">
                    <img id="avatar-img" src="{avatar.get('src', '')}" alt="{avatar.get('alt', '')}" class="w-full h-full object-cover rounded-full">
                </div>
                <div class="absolute -top-2 -right-2 bg-yellow-400 text-white rounded-full w-10 h-10 flex items-center justify-center text-lg shadow-md animate-pulse">
                    ★
                </div>
                <div class="absolute -bottom-2 -left-2 bg-blue-400 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm shadow-md animate-pulse" style="animation-delay: 0.5s;">
                    ♡
                </div>
            </div>
            
            <h1 class="text-4xl md:text-5xl font-bold mb-4 cute-header">
                {header.get('title', '')}
            </h1>
            
            <p class="text-lg text-slate-700 mb-2">
                <i class="fa fa-star text-yellow-400 floating-star"></i>
                {header.get('subtitle', '')}
                <i class="fa fa-star text-blue-400 floating-star" style="animation-delay: 0.5s;"></i>
            </p>
            
            <div class="mt-4 text-sm text-blue-600 font-mono bg-white/60 inline-block px-4 py-2 rounded-full border-2 border-blue-300">
                <span id="system-time"></span>
                <span class="typing-cursor text-yellow-500">★</span>
            </div>
        </header>
        
        <div class="space-y-8">
            {sections_html}
            {self._render_final_warning()}
        </div>
        {self._render_footer()}
    </div>
    {self._render_modals()}
    <div class="cute-toc-container">
        <button class="toc-button" onclick="toggleToc()" title="目录">
            <i class="fa fa-list"></i>
        </button>
        <div class="toc-panel" id="toc-panel">
            <div class="toc-title">
                <i class="fa fa-bookmark mr-2"></i>目录
            </div>
            {self._render_toc()}
        </div>
    </div>
    <div class="scroll-buttons-container">
        <button class="scroll-button top" onclick="scrollToTop()" title="返回顶部">
            <i class="fa fa-arrow-up"></i>
        </button>
        <button class="scroll-button bottom" onclick="scrollToBottom()" title="前往底部">
            <i class="fa fa-arrow-down"></i>
        </button>
    </div>
    {self._generate_javascript()}
</body>
</html>'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'成功生成: {output_path}')


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='生成个人扩列条HTML页面')
    parser.add_argument('--config', '-c', help='用户配置JSON文件路径', default='user_config.json')
    parser.add_argument('--reference', '-r', help='参考配置JSON文件路径（可选）', default='assets/config.json')
    parser.add_argument('--output', '-o', help='输出HTML文件路径', default='output.html')
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    css_path = script_dir.parent / 'assets' / 'basic-styles.css'
    js_path = script_dir.parent / 'assets' / 'script.js'
    
    generator = HTMLGenerator(
        str(css_path), 
        str(js_path), 
        args.config, 
        args.reference
    )
    generator.generate(args.output)


if __name__ == '__main__':
    main()
