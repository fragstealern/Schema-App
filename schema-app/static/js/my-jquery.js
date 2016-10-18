$(document).ready(function () {
    $(".traindiv").fadeOut(100);
    $("#submit").click(function () {
        $(".traindiv").fadeToggle(1000);
    });
});
$(document).ready(function () {
    $("#show-train").fadeIn(2000);
    $("#show-bus").fadeIn(2000);
    $("#show-train").click(function () {
        $(".trainbody").fadeToggle(500);
    });
    $("#show-bus").click(function () {
        $(".busdiv").fadeToggle(500);
    });
});