//modal settings
var modal = document.getElementById('myModal');
var img_list = document.getElementsByClassName('originThumbnails');
for (let i = 0; i < img_list.length; i++) {
    temp = img_list[i];
    temp.onclick = function () {
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
        changed_url01 = origin_url.replace("-1.", "-2.");
        changed_url03 = origin_url.replace("-1.", "-3.");
        changed_url04 = origin_url.replace("-1.", "-4.");

        slides1.src = this.src;
        slides2.src = changed_url01;
        slides3.src = changed_url03;
        slides4.src = changed_url04;

        //change the slides full-size src
        pic1.src = this.src + "/full";
        pic2.src = changed_url01 + "/full";
        pic3.src = changed_url03 + "/full";
        pic4.src = changed_url04 + "/full";
        slides1.click();
    }
}

// get <span> element to set close button
var span = document.getElementById("modalclose");

// click (x) to close modal
span.onclick = function () {
    modal.style.display = "none";
};

// slides showing part
var slideIndex = 1;
showDivs(slideIndex);

function currentDiv(n) {
    showDivs(slideIndex = n);
}

function showDivs(n) {
    var i;
    var x = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("demo");
    if (n > x.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = x.length
    }
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" w3-opacity-off", "");
    }
    x[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " w3-opacity-off";
}

window.onload = function () {
    var box = document.getElementById("box");
    var imgs = box.getElementsByTagName('img');
    for (let i = 0; i < imgs.length; i++) {
        var w = imgs[i].offsetWidth, h = imgs[i].offsetHeight;
        w > h ? imgs[i].style.width = '100%' : imgs[i].style.height = '100%'
    }
};


//function of showing upload messages
var upload_banner = document.getElementById("wrap");
var tester = document.getElementById("upload-filename").innerHTML;
var fail_text = document.getElementById("check").innerHTML;
var upload_close = document.getElementById("close_button");
var file_name = document.getElementById("upload-filename");
var upload_button = document.getElementById('upload-button');

function showing() {
    upload_banner.style.display = 'none';
    upload_banner.style.display.opacity = '0';
    upload_banner.style.display = 'block';
    setTimeout(function () {//fade in animation
        upload_banner.style.opacity = '1.0';
    }, 14);
}


function auto_hiding() {
    setTimeout(function () {//uploading modal hide after 6.000s
        upload_banner.style.opacity = '0';
        upload_banner.style.display = 'none';
        //clear the text in the file-name
        document.getElementById("upload-filename").innerHTML = "";
    }, 6000);
}


function finish_upload() {
    if (!(tester === '')) {
        if (!(fail_text === '')) {
            document.getElementById("uploadTitle").innerHTML = fail_text;
        }

        else {
            document.getElementById("uploadTitle").innerHTML = "1 upload complete";
        }
        showing();
        auto_hiding();
    }
}

/* raise a modal to remind users to select file first */
function remind_selectfile() {
    if ((document.getElementById('file').value === '')) {
        //change the words in the title
        document.getElementById("uploadTitle").innerHTML = "No File Selected";
        //change the words in text
        document.getElementById("upload-filename").innerHTML = "Please select a file before you upload";
        showing();
    }
}

/* get the selected file name */
function showSelectedFile() {
    document.getElementById('file').addEventListener('change', function () {
        //alert('Selected file: ' + this.value);
        if (document.getElementById('file').value === "") {
            upload_banner.style.opacity = '0';
            upload_banner.style.display = 'none';
        }
        else {
            upload_button.style.backgroundColor = 'rgb(60, 114, 242)';
            document.getElementById("uploadTitle").innerHTML = "1 upload selected";
            file_name.innerHTML = this.value.replace(/.*[\/\\]/, '');
            showing();
        }
    });
}


/*close the upload modal using 'x' button */
upload_close.onclick = function () {
    upload_banner.style.display = 'none';
    upload_banner.style.opacity = '0';
    //clear the text in the file-name
    document.getElementById("upload-filename").innerHTML = "";
    tester = "";
};

//when the 'upload' button is clicked, remind users to selecte file first.
upload_button.addEventListener('click', remind_selectfile);

showSelectedFile();
finish_upload();





