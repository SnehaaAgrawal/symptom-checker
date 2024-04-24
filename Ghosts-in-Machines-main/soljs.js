document.addEventListener("DOMContentLoaded", function() {
    const elements = document.querySelectorAll('.animate');
    elements.forEach(element => {
        element.classList.add('active');
    });
});
