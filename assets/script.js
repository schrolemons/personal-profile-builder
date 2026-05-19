
// 个人扩列条页面 JavaScript
// 动态配置变量 (通过 generate.py 设置)
if (typeof window.__config === 'undefined') {
    window.__config = {};
}

// 初始化函数
document.addEventListener('DOMContentLoaded', function() {
    initializeLinks();
    createSparkles();
    updateTime();
    setInterval(updateTime, 1000);
    initializeCarousel();
    startTyping();
});

// 初始化所有链接
function initializeLinks() {
    document.querySelectorAll('a').forEach(link => {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });
}

// 创建星星背景
function createSparkles() {
    const container = document.getElementById('sparkle-bg');
    if (!container) return;
    
    const sparkles = ['★', '☆', '✦', '✧', '♥', '✿', '❀'];
    for (let i = 0; i < 20; i++) {
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle';
        sparkle.textContent = sparkles[Math.floor(Math.random() * sparkles.length)];
        sparkle.style.left = Math.random() * 100 + '%';
        sparkle.style.top = Math.random() * 100 + '%';
        sparkle.style.animationDelay = Math.random() * 3 + 's';
        sparkle.style.fontSize = (Math.random() * 20 + 12) + 'px';
        container.appendChild(sparkle);
    }
}

// 更新系统时间
function updateTime() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('zh-CN', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    const dateStr = now.toLocaleDateString('zh-CN');
    
    const timeElement = document.getElementById('system-time');
    if (timeElement) {
        timeElement.textContent = `[${dateStr} ${timeStr}] ☆`;
    }
}

// 轮播图功能
let galleryStates = {};
let autoPlayIntervals = {};

function getGalleryData(galleryId) {
    const galleries = window.__config.galleries || [];
    return galleries.find(g => g.id === galleryId);
}

function initializeCarousel() {
    const galleries = window.__config.galleries || [];
    if (galleries.length === 0) return;
    
    galleries.forEach(gallery => {
        if (!galleryStates[gallery.id]) {
            galleryStates[gallery.id] = { currentSlide: 0 };
        }
        updateSlide(gallery.id);
        resetAutoPlay(gallery.id);
    });
}

function updateSlide(galleryId) {
    const gallery = getGalleryData(galleryId);
    if (!gallery) return;
    
    const slides = gallery.slides;
    if (!slides || slides.length === 0) return;
    
    const state = galleryStates[galleryId];
    const img = document.getElementById(`${galleryId}-carousel-img`);
    const caption = document.getElementById(`${galleryId}-carousel-caption`);
    const dots = document.querySelectorAll(`.carousel-dot[data-gallery="${galleryId}"]`);
    const feedCounter = document.getElementById(`${galleryId}-feed-counter`);
    
    if (!img || !caption) return;
    
    if (slides[state.currentSlide]) {
        img.src = slides[state.currentSlide].src;
        img.alt = slides[state.currentSlide].alt;
        caption.textContent = slides[state.currentSlide].caption;
        
        if (feedCounter) {
            const feedNum = String(state.currentSlide + 1).padStart(3, '0');
            feedCounter.textContent = feedNum + '/' + String(slides.length).padStart(3, '0');
        }
        
        dots.forEach((dot, index) => {
            if (index === state.currentSlide) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }
}

function nextSlide(galleryId) {
    const gallery = getGalleryData(galleryId);
    if (!gallery) return;
    
    const slides = gallery.slides;
    if (!slides || slides.length === 0) return;
    
    const state = galleryStates[galleryId];
    state.currentSlide = (state.currentSlide + 1) % slides.length;
    updateSlide(galleryId);
    resetAutoPlay(galleryId);
}

function prevSlide(galleryId) {
    const gallery = getGalleryData(galleryId);
    if (!gallery) return;
    
    const slides = gallery.slides;
    if (!slides || slides.length === 0) return;
    
    const state = galleryStates[galleryId];
    state.currentSlide = (state.currentSlide - 1 + slides.length) % slides.length;
    updateSlide(galleryId);
    resetAutoPlay(galleryId);
}

function goToSlide(galleryId, index) {
    const gallery = getGalleryData(galleryId);
    if (!gallery) return;
    
    const slides = gallery.slides;
    if (!slides || slides.length === 0) return;
    
    const state = galleryStates[galleryId];
    state.currentSlide = index;
    updateSlide(galleryId);
    resetAutoPlay(galleryId);
}

function resetAutoPlay(galleryId) {
    if (autoPlayIntervals[galleryId]) {
        clearInterval(autoPlayIntervals[galleryId]);
    }
    autoPlayIntervals[galleryId] = setInterval(() => nextSlide(galleryId), 5000);
}

// 打字效果
function startTyping() {
    const typingElement = document.getElementById('typing-content');
    if (!typingElement) return;
    
    const secretWord = window.__config.secretWord || '';
    const warningContent = window.__config.warningContent || '';
    
    // 替换 {{secret_word}} 为实际的 secretWord
    const processedContent = warningContent.replace(/\{\{secret_word\}\}/g, 
        `<span class="font-bold bg-white px-3 py-1 rounded-full border-2 border-yellow-400 mx-1">${secretWord}</span>`
    );
    
    // 提取文本部分用于打字效果
    let displayText = processedContent;
    // 先保存所有HTML标签，打字时只打文本内容，最后再把HTML放回去
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = processedContent;
    const plainText = tempDiv.textContent || tempDiv.innerText;
    
    let currentIndex = 0;
    
    function type() {
        if (currentIndex <= plainText.length) {
            // 显示当前已打字的部分，同时保留HTML结构
            typingElement.innerHTML = processedContent;
            // 我们简单处理：先直接显示内容，再做光标闪烁
            typingElement.innerHTML = processedContent;
            return;
        }
    }
    
    // 简化处理：直接显示内容
    setTimeout(() => {
        typingElement.innerHTML = processedContent;
    }, 1000);
}

// 头像旋转和夜间模式
let isSpinning = false;
let isNightMode = false;

function spinAvatar() {
    if (isSpinning) return;
    
    const avatar = document.getElementById('avatar-container');
    isSpinning = true;
    
    avatar.classList.remove('spinning');
    void avatar.offsetWidth;
    avatar.classList.add('spinning');
    
    isNightMode = !isNightMode;
    if (isNightMode) {
        document.body.classList.add('night-mode');
    } else {
        document.body.classList.remove('night-mode');
    }
    
    setTimeout(() => {
        isSpinning = false;
    }, 800);
}

// 图片灯箱
function openLightbox(src, alt) {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    
    if (lightboxImg) lightboxImg.src = src;
    if (lightboxCaption) lightboxCaption.textContent = alt;
    
    if (lightbox) {
        lightbox.classList.remove('hidden');
        lightbox.classList.add('flex');
    }
    
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    
    if (lightbox) {
        lightbox.classList.remove('flex');
        lightbox.classList.add('hidden');
    }
    
    document.body.style.overflow = 'auto';
}

// 爱好弹窗
function openHobbyModal(title, icon, content) {
    const modal = document.getElementById('hobby-modal');
    const modalTitle = document.getElementById('hobby-modal-title');
    const modalIcon = document.getElementById('hobby-modal-icon');
    const modalContent = document.getElementById('hobby-modal-content');
    
    if (modalTitle) modalTitle.textContent = title;
    
    if (modalIcon) {
        if (icon.startsWith('fa-')) {
            modalIcon.innerHTML = '<i class="fa ' + icon + '"></i>';
        } else {
            modalIcon.textContent = icon;
        }
    }
    
    if (modalContent) {
        modalContent.innerHTML = '<p>' + content.replace(/\\n/g, '</p><p>') + '</p>';
    }
    
    if (modal) {
        modal.classList.add('active');
    }
    
    document.body.style.overflow = 'hidden';
}

function closeHobbyModal(event) {
    if (event && event.target !== event.currentTarget && !event.target.classList.contains('hobby-modal-close')) {
        return;
    }
    
    const modal = document.getElementById('hobby-modal');
    if (modal) {
        modal.classList.remove('active');
    }
    
    document.body.style.overflow = 'auto';
}

// 性格弹窗
function openPersonalityModal(title, icon, content) {
    const modal = document.getElementById('personality-modal');
    const modalTitle = document.getElementById('personality-modal-title');
    const modalIcon = document.getElementById('personality-modal-icon');
    const modalContent = document.getElementById('personality-modal-content');
    
    if (modalTitle) modalTitle.textContent = title;
    if (modalIcon) modalIcon.innerHTML = '<i class="fa ' + icon + '"></i>';
    
    if (modalContent) {
        modalContent.innerHTML = '<p>' + content.replace(/\\n/g, '</p><p>') + '</p>';
    }
    
    if (modal) {
        modal.classList.add('active');
    }
    
    document.body.style.overflow = 'hidden';
}

function closePersonalityModal(event) {
    if (event && event.target !== event.currentTarget && !event.target.classList.contains('personality-modal-close')) {
        return;
    }
    
    const modal = document.getElementById('personality-modal');
    if (modal) {
        modal.classList.remove('active');
    }
    
    document.body.style.overflow = 'auto';
}

// 关闭确认
let pendingCloseId = null;

function closeSection(id) {
    const sectionIds = window.__config.sectionIds || [];
    const tocMap = window.__config.tocMap || {};
    
    let visibleCount = 0;
    for (let sid of sectionIds) {
        const s = document.getElementById(sid);
        if (s && s.style.display !== 'none') {
            visibleCount++;
        }
    }
    
    if (visibleCount <= 1) {
        pendingCloseId = id;
        document.getElementById('confirm-modal').classList.add('active');
    } else {
        performCloseSection(id, tocMap);
    }
}

function performCloseSection(id, tocMap) {
    const section = document.getElementById(id);
    if (section) {
        section.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        section.style.opacity = '0';
        section.style.transform = 'scale(0.95)';
        
        const tocItemId = tocMap[id];
        const tocItem = document.getElementById(tocItemId);
        if (tocItem) {
            tocItem.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            tocItem.style.opacity = '0';
            tocItem.style.transform = 'translateX(-10px)';
            setTimeout(() => {
                tocItem.style.display = 'none';
            }, 300);
        }
        
        setTimeout(() => {
            section.style.display = 'none';
            checkAllClosed();
        }, 300);
    }
}

function confirmCloseSummary() {
    closeConfirmModal();
    if (pendingCloseId) {
        const tocMap = window.__config.tocMap || {};
        performCloseSection(pendingCloseId, tocMap);
        pendingCloseId = null;
    }
}

function closeConfirmModal(event) {
    if (event && event.target !== event.currentTarget) {
        return;
    }
    document.getElementById('confirm-modal').classList.remove('active');
}

function checkAllClosed() {
    const sectionIds = window.__config.sectionIds || [];
    const warning = document.getElementById('final-warning');
    const footer = document.querySelector('footer');
    
    let allClosed = true;
    sectionIds.forEach(id => {
        const section = document.getElementById(id);
        if (section && section.style.display !== 'none') {
            allClosed = false;
        }
    });
    
    if (allClosed && warning) {
        warning.classList.add('active');
        if (footer) {
            footer.style.display = 'none';
        }
    }
}

// 目录功能
let tocOpen = false;

function toggleToc() {
    tocOpen = !tocOpen;
    const panel = document.getElementById('toc-panel');
    if (tocOpen) {
        panel.classList.add('active');
    } else {
        panel.classList.remove('active');
    }
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
        tocOpen = false;
        document.getElementById('toc-panel').classList.remove('active');
    }
}

// 监听滚动更新目录高亮
window.addEventListener('scroll', function() {
    const sectionIds = window.__config.sectionIds || [];
    const tocItems = document.querySelectorAll('.toc-item');
    
    let currentSection = sectionIds[0];
    sectionIds.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            const rect = section.getBoundingClientRect();
            if (rect.top <= 150) {
                currentSection = sectionId;
            }
        }
    });
    
    tocItems.forEach((item, index) => {
        item.classList.remove('active');
        if (sectionIds[index] === currentSection) {
            item.classList.add('active');
        }
    });
});

// 滚动功能
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function scrollToBottom() {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
}

// 键盘快捷键
document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        // 找到当前视口内的第一个 gallery
        const galleries = window.__config.galleries || [];
        if (galleries.length > 0) {
            let closestGallery = null;
            let minDistance = Infinity;
            
            for (let gallery of galleries) {
                const element = document.querySelector(`[data-gallery="${gallery.id}"]`);
                if (element) {
                    const rect = element.getBoundingClientRect();
                    // 检查是否在视口内
                    if (rect.top < window.innerHeight && rect.bottom > 0) {
                        const distance = Math.abs(rect.top);
                        if (distance < minDistance) {
                            minDistance = distance;
                            closestGallery = gallery;
                        }
                    }
                }
            }
            
            if (closestGallery) {
                if (e.key === 'ArrowLeft') {
                    prevSlide(closestGallery.id);
                } else {
                    nextSlide(closestGallery.id);
                }
            }
        }
    } else if (e.key === 'Escape') {
        closeLightbox();
        closeHobbyModal();
        closePersonalityModal();
        closeConfirmModal();
    }
});
