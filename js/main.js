document.addEventListener('DOMContentLoaded', function () {

    var navItems = document.querySelectorAll('.nav-item');

    if (window.location.pathname.split("/").pop() == 'home.html') {
        navItems[0].classList.add('active');
    }
    if (window.location.pathname.split("/").pop() == 'about.html') {
        navItems[2].classList.add('active');
    }
    if (window.location.pathname.split("/").pop() == 'search.html') {
        navItems[1].classList.add('active-special');
    }

    var logo = document.getElementsByClassName('logoimg');
    logo[0].addEventListener('click', function () {
        window.location.href = 'home.html';
    });
    logo[0].style.cursor = 'pointer';
});
