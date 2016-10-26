$(document).ready(function () {
    $("#tiden").css({"position": "fixed", "top": "0"});
});
$(document).ready(function () {
    'use strict';
    $("#show-train").fadeIn(2000);
    $("#show-bus").fadeIn(2000);
    $("#show-train").click(function () {
        $(".trainbody").fadeToggle(500);
    });
    $("#show-bus").click(function () {
        $(".busdiv").fadeToggle(500);
    });
});