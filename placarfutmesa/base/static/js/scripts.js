// MENU COLLAPSE
const menuToggle = document.getElementById('menuToggle');
const menuList = document.getElementById('menuList');
const navList = document.getElementById('nav-toggle-bx');
menuToggle.addEventListener('click', () => {
    menuList.classList.toggle('collapsed');
    navList.classList.toggle('collapsed');
});


// MENU DROPDOWN
const menuDepartment = document.getElementById('department');
const listDropdown = document.getElementById('listDropdown');
menuDepartment.addEventListener('click', () => {
    listDropdown.classList.toggle('dropdown');
});


// CAROUSEL
const track = document.querySelector('.carousel-track');
const items = document.querySelectorAll('.carousel-item');
const totalItems = items.length;

let currentIndex = 0;

const firstClone = items[0].cloneNode(true);
track.appendChild(firstClone);

function updateCarousel() {
    const width = items[0].offsetWidth;

    currentIndex++;
    track.style.transition = 'transform 0.5s ease-in-out';
    track.style.transform = `translateX(-${currentIndex * width}px)`;

    if (currentIndex === totalItems) {
    setTimeout(() => {
        track.style.transition = 'none'; // Remove a animação
        currentIndex = 0; // Volta ao início
        track.style.transform = `translateX(0)`;
    }, 500); // Deve ser igual à duração da transição (0.5s)
    }
}

setInterval(updateCarousel, 4000);

// Recalcula o tamanho no caso de redimensionamento
window.addEventListener('resize', () => {
    track.style.transform = `translateX(-${currentIndex * items[0].offsetWidth}px)`;
});