// room_modal.js
document.addEventListener('DOMContentLoaded', function () {
    // Обработка клика по карточке комнаты
    function bindRoomCardClicks() {
        document.querySelectorAll('.room-card').forEach(card => {
            card.addEventListener('click', function (e) {
                // Если кликнули по ссылке "Выбрать" — не открываем модалку
                if (e.target.closest('a')) return;

                const roomId = this.dataset.id;
                const checkIn = this.dataset.checkIn;
                const checkOut = this.dataset.checkOut;
                const guests = this.dataset.guests;

                const query = new URLSearchParams({
                    check_in: checkIn,
                    check_out: checkOut,
                    guests: guests
                }).toString();

                fetch(`/rooms/modal/${roomId}?${query}`)
                    .then(response => response.text())
                    .then(html => {
                        const modalContent = document.getElementById('roomModalContent');
                        modalContent.innerHTML = html;
                        new bootstrap.Modal(document.getElementById('roomModal')).show();
                    })
                    .catch(error => {
                        console.error("Ошибка при загрузке модального окна:", error);
                    });
            });
        });
    }

    bindRoomCardClicks();
});

// Обработчик кнопки "Подробнее"
document.addEventListener('click', function (e) {
    if (e.target && e.target.id === 'expandDetailsBtn') {
        const modalBody = e.target.closest('.modal-body');
        if (!modalBody) return;

        const detailsSection = modalBody.querySelector('.room-full-details');
        if (detailsSection) {
            detailsSection.classList.toggle('d-none');
            e.target.textContent = detailsSection.classList.contains('d-none') ? 'Подробнее' : 'Скрыть';
        }
    }
});
