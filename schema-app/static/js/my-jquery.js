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
