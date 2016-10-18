$(document).ready(function () {
    $(".traindiv").fadeOut(100);
    $("#from").click(function () {
        $(".traindiv").fadeToggle(1000);
    });
});