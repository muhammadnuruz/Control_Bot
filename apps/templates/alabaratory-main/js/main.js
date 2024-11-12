// API URLlari
const searchApiUrl = "http://147.45.106.35:8000/api/types/search/";
const analyseApiUrl = "http://147.45.106.35:8000/api/analyses/";

if (window.location.protocol === 'https:') {
    window.location.href = window.location.href.replace('http:', 'https:');
}


// Type qidirish funksiyasi
function searchType() {
    const searchText = document.getElementById('searchText').value;

    if (!searchText) {
        alert('Please enter search text!');
        return;
    }

    const typeResultDiv = document.getElementById('typeResult');
    typeResultDiv.innerHTML = '';

    // APIga so'rov yuborish
    fetch(`${searchApiUrl}${searchText}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('No types found');
            }
            return response.json();
        })
        .then(data => {
            // data.results arrayga tekshirish
            if (!Array.isArray(data.results)) {
                throw new Error('Unexpected response format');
            }

            if (data.results.length === 0) {
                typeResultDiv.innerHTML = '<p>Bunday tahlil topilmadi</p>';
                return;
            }

            const list = document.createElement('ul');
            data.results.forEach(item => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `ID: ${item.id}<br> Nomi: ${item.name}<br> Narxi: ${item.price}<br> Ma'lumot: ${item.info}<br> Tayyor bo'lish vaqti: ${item.to_be_ready} kun`;
                list.appendChild(listItem);
            });
            typeResultDiv.appendChild(list);
        })
        .catch(error => {
            typeResultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        });
}

// Analyse ma'lumotini olish funksiyasi
function getAnalysis() {
    const analyseId = document.getElementById('analyseId').value;

    if (!analyseId) {
        alert('Laboratoriya tomonidan berilgan IDni kiriting!');
        return;
    }

    const analyseResultDiv = document.getElementById('analyseResult');
    analyseResultDiv.innerHTML = '';

    // APIga so'rov yuborish
    fetch(`${analyseApiUrl}${analyseId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Tahlil topilmadi');
            }
            return response.json();
        })
        .then(data => {
            const analyseDiv = document.createElement('div');
            analyseDiv.classList.add('result');

            analyseDiv.innerHTML = `
                <h3>Analysis ID: ${data.id}</h3>
                <p><strong>Tahlil tayyor bo'lgan vaqt:</strong> ${new Date(data.created_at).toLocaleString()}</p>
                <a href="${data.file}" target="_blank">PDF Yuklab olish</a>
            `;

            analyseResultDiv.appendChild(analyseDiv);
        })
        .catch(error => {
            analyseResultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        });
}

(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Date and time picker
    $('.date').datetimepicker({
        format: 'L'
    });
    $('.time').datetimepicker({
        format: 'LT'
    });


    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: false,
        animateOut: 'fadeOutLeft',
        items: 1,
        dots: true,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: false,
        smartSpeed: 1000,
        center: true,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            }
        }
    });

    
})(jQuery);