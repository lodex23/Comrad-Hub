document.addEventListener('DOMContentLoaded', function () {
    const userButton = document.querySelector('.user-button');
    const dropdownMenu = document.querySelector('.user-dropdown');

    // Toggle dropdown on button click
    userButton.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevent click from closing the dropdown immediately
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });

    // Hide dropdown when clicking outside of it
    document.addEventListener('click', function () {
        dropdownMenu.style.display = 'none';
    });

    // Hide dropdown on mouse leave
    dropdownMenu.addEventListener('mouseleave', function () {
        dropdownMenu.style.display = 'none';
    });
});
