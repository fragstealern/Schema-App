/*Den första delen här i dokumentet är till tåget och bussen*/  
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

$(document).ready(function(){
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal-trigger').leanModal();
  });
