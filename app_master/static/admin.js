// real-time range value showing
var scaleUp = document.getElementById('manualScaleUp');
var scaleUpRatio = document.getElementById('scaleUpRatio');
var scaleDownRatio = document.getElementById('scaleDownRatio');
var scaleUpValue = document.getElementById('manualScaleUpShowing');
var scaleDownRatioShowing = document.getElementById('scaleDownRatioShowing');
var scaleUpRatioShowing = document.getElementById('scaleUpRatioShowing');
setInterval(function () {
    scaleUpValue.innerHTML = scaleUp.value;
    scaleDownRatioShowing.innerHTML = scaleDownRatio.value + "%";
    scaleUpRatioShowing.innerHTML = scaleUpRatio.value + "%";
}, 0.01);
