$(document).ready(function () {
    $("#findTime").on('submit', function () {
        $('html, body').animate({
            scrollTop: $("#tiden").offset().top
        }, 1000);
        return false;
    });
});
    
$(document).ready(function () {
    'use strict';
    $("#show-train").fadeIn(5000);
    $("#show-bus").fadeIn(5000);
    $("#show-train").click(function () {
        $(".trainbody").fadeToggle(500);
    });
    $("#show-bus").click(function () {
        $(".busdiv").fadeToggle(500);
    });
});