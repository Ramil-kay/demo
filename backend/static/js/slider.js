

(function() {
    // Проверяем наличие слайдера на странице
    const sliderContainer = document.querySelector('.slider-container');
    if (!sliderContainer) return;
    
    let currentSlide = 0;
    let autoSlideInterval;
    let isPaused = false;
    let isTransitioning = false; // Флаг для предотвращения множественных переходов
    const slides = document.querySelectorAll('.slide');
    
    if (slides.length === 0) return;
    
    /**
     * Показать слайд по индексу
     * @param {number} n - индекс слайда
     */
    function showSlide(n) {
        // Предотвращаем множественные вызовы во время анимации
        if (isTransitioning) return;
        
        isTransitioning = true;
        
        // Убираем активный класс у всех слайдов
        slides.forEach(slide => slide.classList.remove('active'));
        
        // Вычисляем корректный индекс
        currentSlide = (n + slides.length) % slides.length;
        
        // Добавляем активный класс текущему слайду
        slides[currentSlide].classList.add('active');
        
        // Обновляем точки (dots) если они есть
        const dots = document.querySelectorAll('.dot');
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentSlide);
        });
        
        // Снимаем флаг блокировки через время анимации
        setTimeout(() => {
            isTransitioning = false;
        }, 500);
    }
    
    /**
     * Переключение на следующий слайд
     */
    function nextSlide() {
        if (isTransitioning) return;
        showSlide(currentSlide + 1);
    }
    
    /**
     * Переключение на предыдущий слайд
     */
    function prevSlide() {
        if (isTransitioning) return;
        showSlide(currentSlide - 1);
    }
    
    /**
     * Запуск автоматической смены слайдов (каждые 3 секунды)
     */
    function startAutoSlide() {
        stopAutoSlide();
        autoSlideInterval = setInterval(() => {
            // Автопереключение работает только если не наведена мышь и не в процессе перехода
            if (!isPaused && !isTransitioning) {
                showSlide(currentSlide + 1);
            }
        }, 3000);
    }
    
    /**
     * Остановка автоматической смены слайдов
     */
    function stopAutoSlide() {
        if (autoSlideInterval) {
            clearInterval(autoSlideInterval);
            autoSlideInterval = null;
        }
    }
    
    /**
     * Сброс таймера при взаимодействии пользователя
     */
    function resetTimer() {
       
        startAutoSlide();
    }
    
    /**
     * Пауза при наведении
     */
    function pauseSlider() {
        isPaused = true;
    }
    
    /**
     * Возобновление при уходе мыши
     */
    function resumeSlider() {
        isPaused = false;
    }
    
    // Создаем точки навигации (dots)
    function createDots() {
        const dotsContainer = document.getElementById('sliderDots');
        if (!dotsContainer) return;
        
        dotsContainer.innerHTML = '';
        slides.forEach((_, i) => {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (!isTransitioning) {
                    showSlide(i);
                    resetTimer();
                }
            });
            dotsContainer.appendChild(dot);
        });
    }
    
    // Добавляем обработчики для кнопок
    function addButtonHandlers() {
        const prevBtn = document.getElementById('sliderPrev');
        const nextBtn = document.getElementById('sliderNext');
        
        if (prevBtn) {
            // Удаляем старые обработчики, чтобы не было дублирования
            const newPrevBtn = prevBtn.cloneNode(true);
            prevBtn.parentNode.replaceChild(newPrevBtn, prevBtn);
            
            newPrevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (!isTransitioning) {
                    prevSlide();
                    resetTimer();
                }
                return false;
            });
        }
        
        if (nextBtn) {
            // Удаляем старые обработчики, чтобы не было дублирования
            const newNextBtn = nextBtn.cloneNode(true);
            nextBtn.parentNode.replaceChild(newNextBtn, nextBtn);
            
            newNextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (!isTransitioning) {
                    nextSlide();
                    resetTimer();
                }
                return false;
            });
        }
    }
    
    // Добавляем обработчики для паузы при наведении
    function addHoverHandlers() {
        // Останавливаем автопереключение при наведении на слайдер
        sliderContainer.addEventListener('mouseenter', pauseSlider);
        sliderContainer.addEventListener('mouseleave', resumeSlider);
        
        // Для мобильных устройств
        sliderContainer.addEventListener('touchstart', pauseSlider);
        sliderContainer.addEventListener('touchend', () => {
            setTimeout(resumeSlider, 3000);
        });
    }
    
    // Добавляем поддержку клавиатуры
    function addKeyboardSupport() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                prevSlide();
                resetTimer();
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                nextSlide();
                resetTimer();
            }
        });
    }
    
    // Инициализация
    function initSlider() {
        createDots();
        addButtonHandlers();
        addHoverHandlers();
        addKeyboardSupport();
        startAutoSlide();
    }
    
    // Запускаем слайдер после полной загрузки DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSlider);
    } else {
        initSlider();
    }
})();