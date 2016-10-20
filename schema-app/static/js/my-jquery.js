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

var tday=new Array("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday");
var tmonth=new Array("January","February","March","April","May","June","July","August","September","October","November","December");

function GetClock(){
var d=new Date();
var nday=d.getDay(),nmonth=d.getMonth(),ndate=d.getDate();
var nhour=d.getHours(),nmin=d.getMinutes(),nsec=d.getSeconds();
if(nmin<=9) nmin="0"+nmin
if(nsec<=9) nsec="0"+nsec;

document.getElementById('timeDisplay').innerHTML=""+tday[nday]+", "+tmonth[nmonth]+" "+ndate+" "+nhour+":"+nmin+":"+nsec+"";
}

window.onload=function(){
GetClock();
setInterval(GetClock,1000);
}