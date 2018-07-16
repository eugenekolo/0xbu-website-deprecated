jQuery(function($) {

    /* ============================================================ */
    /* Responsive Videos */
    /* ============================================================ */

    $(".post-content").fitVids();

    /* ============================================================ */
    /* Scroll To Top */
    /* ============================================================ */

    $('.js-jump-top').on('click', function(e) {
        e.preventDefault();

        $('html, body').animate({'scrollTop': 0});
    });
});


function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    else
    {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = dc.length;
        }
    }

    return decodeURI(dc.substring(begin + prefix.length, end));
}

function check_nightmode() {
    var nightmode = getCookie("nightmode");

    if (nightmode === "true") {
        document.body.classList.toggle('nightmode');
    }
}

check_nightmode();

$(window).load(function() {
    var nightmode = getCookie("nightmode");

    if (nightmode === "true") {
        document.getElementById('feather-path').classList.toggle('nightmode-feather');
    }
});
