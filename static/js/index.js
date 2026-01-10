        let currentIndex = 0; 
        const cards = document.querySelectorAll('.movie-card');
        const totalCards = cards.length;

        function getWrappedIndex(index) {
            return (index + totalCards) % totalCards;
        }

        function updateCarousel() {
            cards.forEach(card => {
                card.style.display = 'none';
                card.classList.remove('active');
                card.style.order = '0'; 
            });

            const prevIndex = getWrappedIndex(currentIndex - 1);
            const nextIndex = getWrappedIndex(currentIndex + 1);

            const prevCard = cards[prevIndex];
            const currCard = cards[currentIndex];
            const nextCard = cards[nextIndex];

            // 左
            prevCard.style.display = 'flex';
            prevCard.style.order = '1';

            // 中央
            currCard.style.display = 'flex';
            currCard.style.order = '2';
            currCard.classList.add('active');

            // 右
            nextCard.style.display = 'flex';
            nextCard.style.order = '3';
        }

        function moveSlide(direction) {
            currentIndex = getWrappedIndex(currentIndex + direction);
            updateCarousel();
        }

        function selectMovie(id) {
            location.href = "/booking?movie_id=" + encodeURIComponent(id);
        }

        updateCarousel();