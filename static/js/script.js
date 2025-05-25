document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('id_comment');
    const counter = document.getElementById('char-counter');
    const form = textarea.closest('form');

    // Счетчик символов
    textarea.addEventListener('input', function() {
        const currentLength = this.value.length;
        counter.textContent = `${currentLength}/500`;

        if (currentLength > 500) {
            this.classList.add('is-invalid');
        } else {
            this.classList.remove('is-invalid');
        }
    });

    // Валидация при отправке формы
    form.addEventListener('submit', function(e) {
        if (textarea.value.trim() === '' || textarea.value.length > 500) {
            e.preventDefault();
            textarea.classList.add('is-invalid');
            textarea.focus();
        }
    });
});