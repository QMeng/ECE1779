//modal settings
var modal = document.getElementById('myModal');
var img_list = document.getElementsByClassName('originThumbnails');
preloadedSong = new Audio();
for (let i = 0; i < img_list.length; i++) {
    var temp = img_list[i];
    temp.onclick = function (event) {
        //change the pic src
        modal.style.display = "block";
        pic1 = document.getElementById("pic01");
        // grab the urls from hidden elements
        img_name = this.id;

        var type = (img_name + '').split('thumbnail-')[0];
        var basename = (img_name + '').split('thumbnail-')[1];
        var singlename =(basename + '').split('.')[0];
        image1_url = document.getElementById("image-" + basename).getAttribute("value");

        // re-assign the src of the elements
        pic1.src = image1_url;
        document.getElementById('single-title').innerHTML = singlename;
        document.getElementById('song').innerHTML = singlename;

        preloadedSong.src = document.getElementById('music-'+ basename).getAttribute("value");
        //document.getElementById('mainAudio').src = document.getElementById('music-'+ basename).getAttribute("value");
    }
}

// get <span> element to set close button
var span = document.getElementById("modalclose");

// click (x) to close modal
span.onclick = function () {
    modal.style.display = "none";
};

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
var music_button = document.getElementById('viewMusic');
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
            //window.location.replace("../home");
        }

        else {
            document.getElementById("uploadTitle").innerHTML = "1 upload complete";
        }
        showing();
        auto_hiding();
        tester = "";
    }
}

/* raise a modal to remind users to select file first */
function remind_selectfile() {
    if ((document.getElementById('image').value === '')) {
        //change the words in the title
        document.getElementById("uploadTitle").innerHTML = "No image Selected";
        //change the words in text
        document.getElementById("upload-filename").innerHTML = "Please select an image before you upload";
        showing();
    }
    else if ((document.getElementById('music').value === '')) {
        //change the words in the title
        //setTimeout(function(){music_button.style.backgroundColor = 'rgba(60, 114, 242, 80)';},10);
        document.getElementById("uploadTitle").innerHTML = "No music Selected";
        //change the words in text
        document.getElementById("upload-filename").innerHTML = "Please select a music before you upload";
        showing();
    }
    else{
        //setTimeout(function(){music_button.style.backgroundColor = 'rgba(60, 114, 242, 80)';},10);
        //setTimeout(function(){upload_button.style.backgroundColor = 'rgba(60, 114, 242, 80)';},10);
    }
}

/* get the selected image name */
function showSelectedImage() {
    document.getElementById('image').addEventListener('change', function () {
        //alert('Selected file: ' + this.value);
        if (document.getElementById('image').value === "") {
            upload_banner.style.opacity = '0';
            upload_banner.style.display = 'none';
        }
        else {
            //setTimeout(function(){music_button.style.backgroundColor = 'rgba(60, 114, 242, 80)';},10);
            document.getElementById("uploadTitle").innerHTML = "1 upload selected";
            file_name.innerHTML = this.value.replace(/.*[\/\\]/, '');
            showing();
            checkUploadButton();
        }
    });
}

/* get the selected music name */
function showSelectedMusic() {
    document.getElementById('music').addEventListener('change', function () {
        //alert('Selected file: ' + this.value);
        if (document.getElementById('music').value === "") {
            upload_banner.style.opacity = '0';
            upload_banner.style.display = 'none';
        }
        else {
            document.getElementById("uploadTitle").innerHTML = "1 upload selected";
            file_name.innerHTML = this.value.replace(/.*[\/\\]/, '');
            showing();
            checkUploadButton();
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

/* ban click event of select music (currently not used) */
function checkUploadButton(){
     if (document.getElementById('image').value != "" && document.getElementById('music').value != ""){
        setTimeout(function(){upload_button.style.backgroundColor = 'rgba(60, 114, 242, 80)';},10);
     }
}

//when the 'upload' button is clicked, remind users to selecte file first.
//banClickMusicButton();
upload_button.addEventListener('click', remind_selectfile);
//music_button.addEventListener('click', remind_selectfile);
showSelectedImage();
showSelectedMusic();
finish_upload();

/*play button function */

//var playButton = document.getElementById('triangle');
//var audioTest = document.getElementById('hego-1');
//need a for loop to make all the function works
var uploadedMusics = document.getElementsByClassName('uploadedMusics');
var playButtons = document.getElementsByClassName('playButtons');
for (let i = 0; i < uploadedMusics.length; i++) {
    //var temp = uploadedMusics[i];
    //var playButton = playButtons[i];
    playButtons[i].onclick = function () {
        var sounds = document.getElementsByTagName('audio');
        for(j=0; j<sounds.length; j++){
        if(sounds[j]==uploadedMusics[i]){
        }
        else{
            sounds[j].pause();
        }
        }
        if(uploadedMusics[i].paused){
            uploadedMusics[i].play();
            playButtons[i].src = "../static/Pause.png";
        }
        else{
            uploadedMusics[i].pause();
            playButtons[i].src = "../static/Play.png";
        }
    }
}

/* play in the modal*/
var songBlock = document.getElementById('song-info');
songBlock.onclick = function() {
    var sounds = document.getElementsByClassName('uploadedMusics');
    for(j=0; j<sounds.length; j++){
        if(document.getElementById('mainAudio')==sounds[j]){
        }
        else{
            sounds[j].pause();
        }
    }
     if(document.getElementById('mainAudio').paused){
        if(document.getElementById('mainAudio').src == preloadedSong.src){
            document.getElementById('mainAudio').play();
        }
        else{
            document.getElementById('mainAudio').src = preloadedSong.src;
            document.getElementById('mainAudio').play();
        }
    }
    else{
        if(document.getElementById('mainAudio').src == preloadedSong.src){
            document.getElementById('mainAudio').pause();
        }
        else{
            document.getElementById('mainAudio').src = preloadedSong.src;
            document.getElementById('mainAudio').play();
        }
    }
}

/* control bar */
var pastime = document.getElementById("pastime");
var interval = setInterval(function() {
    var widthline = Math.round(document.getElementById('mainAudio').currentTime)/Math.round(document.getElementById('mainAudio').duration) * 100;
    pastime.style.width = widthline + "%";
    //currentTime.innerHTML = parseInt(Math.round(firstTest.currentTime)/60)+ ":"+Math.round(firstTest.currentTime)%60;
    var totalTime = Math.round(preloadedSong.duration);
    var miniteShowing = Math.round(totalTime/60);
    var secondShowing = Math.round(totalTime%60);
    if (secondShowing < 10){
        document.getElementById('songTime').innerHTML = miniteShowing + ':0' + secondShowing;
    }
    else{
        document.getElementById('songTime').innerHTML = miniteShowing + ':' + secondShowing;
    }
},1000);

/* song duration */

