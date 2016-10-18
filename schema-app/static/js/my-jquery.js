$(document).ready(function () {
    $(".traindiv").fadeOut(100);
    $("#submit").click(function () {
        $(".traindiv").fadeToggle(1000);
    });
});