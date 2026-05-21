/**
 * Слайдер для главной страницы
 * Автоматическая смена изображений каждые 3 секунды
 * Поддержка кнопок "Вперед" и "Назад"
 */

(function() {
    // Проверяем наличие слайдера на странице
    const sliderContainer = document.querySelector('.slider-container');
    if (!sliderContainer) return;
    
    let currentSlide = 0;
    let autoSlideInterval;
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
        showSlide(currentSlide + 1);
    }
    
    /**
     * Переключение на предыдущий слайд
     */
    function prevSlide() {
        showSlide(currentSlide - 1);
    }
    
    /**
     * Запуск автоматической смены слайдов
     */
    function startAutoSlide() {
        stopAutoSlide(); // Останавливаем предыдущий интервал
        autoSlideInterval = setInterval(nextSlide, 3000);
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
            prevBtn.addEventListener('click', () => {
                prevSlide();
                resetTimer();
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                nextSlide();
                resetTimer();
            });
        }
    }
    
    // Инициализация
    function initSlider() {
        createDots();
        addButtonHandlers();
        startAutoSlide();
        
        // Останавливаем автосмену при наведении на слайдер
        sliderContainer.addEventListener('mouseenter', stopAutoSlide);
        sliderContainer.addEventListener('mouseleave', startAutoSlide);
        
        // Для мобильных устройств
        sliderContainer.addEventListener('touchstart', stopAutoSlide);
        sliderContainer.addEventListener('touchend', startAutoSlide);
    }
    
    // Запускаем слайдер после загрузки DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSlider);
    } else {
        initSlider();
    }
})();