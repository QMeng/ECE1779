// 获取弹窗
var modal = document.getElementById('myModal');

// 获取图片插入到弹窗 - 使用 "alt" 属性作为文本部分的内容
var img = document.getElementById('myImg');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
var img_list = document.getElementsByClassName('originThumbnails');
var slides_list = document.getElementsByClassName("demo w3-opacity w3-hover-opacity-off")
for(var i=0; i<img_list.length; i++){
    temp = img_list[i];
    temp.onclick = function(){
        //change the pic src
        modal.style.display = "block";
        picmiddle = document.getElementById("pic02");
        picmiddle.src = this.src+"/full";
        captionText.innerHTML = this.alt;
        //change the slides thumbnail src
        slidesmiddle = document.getElementById("slide02");
        slidesleft = document.getElementById("slide01");
        slidesright = document.getElementById("slide03");
        slidesmiddle.src = this.src;
        origin_url = this.src;
        changed_url01 = origin_url.replace("-1.","-2.");
        changed_url03 = origin_url.replace("-1.","-3.");
        slidesleft.src = changed_url01;
        slidesright.src = changed_url03;
        //change the slides full-size src
        picleft = document.getElementById("pic01");
        picright = document.getElementById("pic03");
        picleft.src = changed_url01 + "/full";
        picright.src = changed_url03 + "/full";
    }
}

// 获取 <span> 元素，设置关闭按钮
var span = document.getElementsByClassName("close")[0];

// 当点击 (x), 关闭弹窗
span.onclick = function() {
  modal.style.display = "none";
}


var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function currentDiv(n) {
  showDivs(slideIndex = n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("demo");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
     dots[i].className = dots[i].className.replace(" w3-opacity-off", "");
  }
  x[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " w3-opacity-off";
}
