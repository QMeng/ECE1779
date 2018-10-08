//modal settings
var modal = document.getElementById('myModal');
var img_list = document.getElementsByClassName('originThumbnails');
for(var i=0; i<img_list.length; i++){
    temp = img_list[i];
    temp.onclick = function(){
        //change the pic src
        modal.style.display = "block";
        pic4 = document.getElementById("pic04");
        pic3 = document.getElementById("pic03");
        pic2 = document.getElementById("pic02");
        pic1 = document.getElementById("pic01");

        //change the slides thumbnail src
        slides2 = document.getElementById("slide02");
        slides1 = document.getElementById("slide01");
        slides3 = document.getElementById("slide03");
        slides4 = document.getElementById("slide04");
        origin_url = this.src;
        changed_url01 = origin_url.replace("-1.","-2.");
        changed_url03 = origin_url.replace("-1.","-3.");
        changed_url04 = origin_url.replace("-1.","-4.");

        slides1.src = this.src;
        slides2.src = changed_url01;
        slides3.src = changed_url03;
        slides4.src = changed_url04;

        //change the slides full-size src
        pic1.src = this.src+"/full";
        pic2.src = changed_url01 + "/full";
        pic3.src = changed_url03 + "/full";
        pic4.src = changed_url04 + "/full";
    }
}
// get <span> element to set close button
var span = document.getElementsByClassName("close")[0];

// click (x) to close modal
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


