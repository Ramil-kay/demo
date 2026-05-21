/**
 * Обработка отзывов на странице бронирований
 */

(function() {
    // Проверяем наличие кнопок для отзывов
    const reviewTriggers = document.querySelectorAll('.btn-review-trigger');
    if (reviewTriggers.length === 0) return;
    
    /**
     * Показать форму отзыва
     * @param {HTMLElement} formContainer - контейнер с формой
     */
    function showReviewForm(formContainer) {
        formContainer.classList.remove('hidden');
    }
    
    /**
     * Скрыть форму отзыва
     * @param {HTMLElement} formContainer - контейнер с формой
     */
    function hideReviewForm(formContainer) {
        formContainer.classList.add('hidden');
    }
    
    /**
     * Получить ID бронирования из элемента
     * @param {HTMLElement} element - элемент с data-booking-id
     * @returns {string} ID бронирования
     */
    function getBookingId(element) {
        return element.dataset.bookingId || element.dataset.appId;
    }
    
    // Добавляем обработчики для кнопок "Оставить отзыв"
    reviewTriggers.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const bookingId = getBookingId(this);
            const formContainer = document.getElementById(`review-form-${bookingId}`);
            if (formContainer) {
                // Скрываем все другие формы
                document.querySelectorAll('.review-form-container').forEach(form => {
                    if (form.id !== `review-form-${bookingId}`) {
                        hideReviewForm(form);
                    }
                });
                // Показываем нужную форму
                showReviewForm(formContainer);
            }
        });
    });
    
    // Добавляем обработчики для кнопок "Отмена"
    const cancelButtons = document.querySelectorAll('.btn-cancel-review');
    cancelButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const bookingId = getBookingId(this);
            const formContainer = document.getElementById(`review-form-${bookingId}`);
            if (formContainer) {
                hideReviewForm(formContainer);
                // Очищаем форму при отмене
                const form = formContainer.querySelector('form');
                if (form) form.reset();
            }
        });
    });
    
    // Валидация формы отзыва перед отправкой
    const reviewForms = document.querySelectorAll('.review-form-container form');
    reviewForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const rating = form.querySelector('select[name="rating"]');
            const comment = form.querySelector('textarea[name="comment"]');
            
            if (rating && !rating.value) {
                e.preventDefault();
                alert('Пожалуйста, выберите оценку');
                rating.focus();
                return false;
            }
            
            if (comment && !comment.value.trim()) {
                e.preventDefault();
                alert('Пожалуйста, введите комментарий');
                comment.focus();
                return false;
            }
        });
    });
    
    // Автоматическое скрытие сообщений через 5 секунд
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.classList.remove('show');
            setTimeout(() => {
                if (message.parentNode) message.remove();
            }, 300);
        }, 5000);
    });
})();