let currentIndex = 0;
const items = document.querySelectorAll('.game-carousel .game');
const totalItems = items.length;
const itemsPerView = 2; // Number of items you want to view at once

document.querySelector('.next-button').addEventListener('click', () => {
    // Update by itemsPerView instead of one item
    if (currentIndex < totalItems - itemsPerView) {
        currentIndex += itemsPerView;
        if (currentIndex > totalItems - itemsPerView) {
            currentIndex = totalItems - itemsPerView;
        }
        updateCarousel();
    }
});

document.querySelector('.prev-button').addEventListener('click', () => {
    // Update by itemsPerView instead of one item
    if (currentIndex > 0) {
        currentIndex -= itemsPerView;
        if (currentIndex < 0) {
            currentIndex = 0;
        }
        updateCarousel();
    }
});

function updateCarousel() {
    const carouselContainer = document.querySelector('.game-carousel');
    const itemStyle = getComputedStyle(items[0]);
    const itemMargin = parseFloat(itemStyle.marginLeft) + parseFloat(itemStyle.marginRight);
    // Calculate the width of a single item
    const itemWidth = items[0].offsetWidth + itemMargin;
    

    // Calculate the total translation based on the current index and itemsPerView
    const translateXValue = currentIndex * itemWidth;

    // Apply the translation to the carousel container
    carouselContainer.style.transform = `translateX(-${translateXValue}px)`;

    // Debugging: Print the total width and item width
    console.log('Total Scrollable Width:', carouselContainer.scrollWidth);
    console.log('Calculated Item Width:', itemWidth);

    // Disable or enable the prevButton button
    const prevButton = document.querySelector('.prevButton');
    prevButton.disabled = currentIndex === 0;

    // Disable or enable the nextButton button
    const nextButton = document.querySelector('.nextButton');
    nextButton.disabled = currentIndex >= totalItems - itemsPerView;
}

const carouselContainer = document.querySelector('.game-carousel');
let startX = 0; // Starting X position of touch
let currentTranslate = 0; // Current translate value
let prevTranslate = 0; // Previous translate value
let isDragging = false;

// Add touch event listeners
carouselContainer.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
    isDragging = true;
    carouselContainer.style.transition = 'none'; // Disable smooth transition for dragging
});

carouselContainer.addEventListener('touchmove', (e) => {
    if (!isDragging) return;

    const currentX = e.touches[0].clientX;
    const deltaX = currentX - startX; // Difference between current and start positions
    currentTranslate = prevTranslate + deltaX; // Calculate new translate value

    // Move the carousel based on touch movement
    carouselContainer.style.transform = `translateX(${currentTranslate}px)`;
});

carouselContainer.addEventListener('touchend', () => {
    isDragging = false;
    const itemStyle = getComputedStyle(items[0]);
    const itemMargin = parseFloat(itemStyle.marginLeft) + parseFloat(itemStyle.marginRight);
    const itemWidth = items[0].offsetWidth + itemMargin;

    // Snap to the nearest item
    const threshold = itemWidth / 2; // Minimum movement to change index
    const movedBy = currentTranslate - prevTranslate;

    if (movedBy > threshold && currentIndex > 0) {
        currentIndex -= itemsPerView; // Move to the previous set of items
    } else if (movedBy < -threshold && currentIndex < totalItems - itemsPerView) {
        currentIndex += itemsPerView; // Move to the next set of items
    }

    // Prevent index out of bounds
    if (currentIndex < 0) currentIndex = 0;
    if (currentIndex > totalItems - itemsPerView) currentIndex = totalItems - itemsPerView;

    updateCarousel();
    prevTranslate = -currentIndex * itemWidth; // Update previous translate value
});

// Update carousel dynamically on window resize
window.addEventListener('resize', () => {
    updateCarousel();
});
// Initialize button visibility
updateCarousel();

