$(document).ready(function () {
    $(".traindiv").fadeOut(100);
    $("#header1").click(function () {
        $(".traindiv").fadeToggle(1000);
    });
});