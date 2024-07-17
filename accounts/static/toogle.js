document.addEventListener("DOMContentLoaded", function() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const menuItems = document.querySelectorAll('.menu-item');

    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });

    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            sidebar.classList.remove('active');
        });
    });
});
