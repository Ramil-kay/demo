

(function() {
    const sliderContainer = document.querySelector('.slider-container');
    if (!sliderContainer) return;
    
    let currentSlide = 0;
    let autoSlideInterval;
    let isPaused = false;
    const slides = document.querySelectorAll('.slide');
    
    if (slides.length === 0) return;
    
    /**
     * Показать слайд по индексу
     * @param {number} n - индекс слайда
     */
    function showSlide(n) {
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
    }
    
    /**
     * Переключение на следующий слайд
     */
    function nextSlide() {
        if (!isPaused) {
            showSlide(currentSlide + 1);
        }
    }
    
    /**
     * Переключение на предыдущий слайд
     */
    function prevSlide() {
        if (!isPaused) {
            showSlide(currentSlide - 1);
            resetTimer(); // Сбрасываем таймер при ручном переключении
        }
    }
    
    /**
     * Запуск автоматической смены слайдов (каждые 3 секунды)
     */
    function startAutoSlide() {
        stopAutoSlide(); // Останавливаем предыдущий интервал
        autoSlideInterval = setInterval(() => {
            if (!isPaused) {
                showSlide(currentSlide + 1);
            }
        }, 3000); // 3000 миллисекунд = 3 секунды
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
        if (autoSlideInterval) {
            stopAutoSlide();
            startAutoSlide();
        }
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
            dot.addEventListener('click', () => {
                showSlide(i);
                resetTimer();
            });
            dotsContainer.appendChild(dot);
        });
    }
    
    // Добавляем обработчики для кнопок
    function addButtonHandlers() {
        const prevBtn = document.getElementById('sliderPrev');
        const nextBtn = document.getElementById('sliderNext');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                prevSlide();
                resetTimer();
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                nextSlide();
                resetTimer();
            });
        }
    }
    
    // Добавляем обработчики для паузы при наведении
    function addHoverHandlers() {
        sliderContainer.addEventListener('mouseenter', pauseSlider);
        sliderContainer.addEventListener('mouseleave', resumeSlider);
        
        // Для мобильных устройств - пауза при касании
        sliderContainer.addEventListener('touchstart', pauseSlider);
        sliderContainer.addEventListener('touchend', () => {
            setTimeout(resumeSlider, 3000); // Возобновляем через 3 секунды после касания
        });
    }
    
    // Инициализация
    function initSlider() {
        createDots();
        addButtonHandlers();
        addHoverHandlers();
        startAutoSlide(); // Запускаем автопереключение каждые 3 секунды
    }
    
    // Запускаем слайдер после загрузки DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSlider);
    } else {
        initSlider();
    }
})();