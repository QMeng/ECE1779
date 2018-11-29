/* showing the first picture in the playlist */
var pics = document.getElementsByClassName('pics');
var artists = document.getElementsByClassName('artists');
function showFirstPic(){
    if (pics.length != 0){
        document.getElementById('pic01').src = '';
        document.getElementById('pic01').src = pics[0].getAttribute('value');
        document.getElementById('single-artist').innerHTML = artists[0].getAttribute('value');
    }
    else{
        document.getElementById('right').style.display = 'none';
        document.getElementById('single-info').style.textAlign = 'center';
        document.getElementById('single-title').innerHTML = 'No music here.'
        document.getElementById('single-artist').innerHTML = 'Unknown';
    }
}
showFirstPic();

/*play button function */
var playButtons = document.getElementsByClassName('playButtons');
function showAllPlayButton(){
    for(i=0; i<playButtons.length; i++){
        playButtons[i].src = "../static/Play.png";
    }
}

/* fill each song block with audio url */
var songBlocks = document.getElementsByClassName('song-info');
clickedSong = new Audio();
preloadedSong = new Audio();
currentBlockId = '';

for (i=0; i<songBlocks.length; i++){
    songBlocks[i].onclick = function(){
        var musicName = this.id;
        thisPlaybutton = document.getElementById("playbutton-" + musicName);
        var pastimes = document.getElementsByClassName('pastime');
        currentBlockId = this;
        for (i=0; i<pastimes.length; i++){
            pastimes[i].style.display = 'none';
        }
        preloadedSong.src = document.getElementById("music-" + musicName).getAttribute("value");
        document.getElementById('pic01').src = document.getElementById("image-" + musicName).getAttribute("value");
        document.getElementById('single-artist').innerHTML = document.getElementById("artist-" + musicName).getAttribute('value');
        var pastime = document.getElementById("pastime-" + musicName);
        showAllPlayButton();
        if (clickedSong.paused){
            if(preloadedSong.src == clickedSong.src){
                clickedSong.play();
                thisPlaybutton.src = '../static/Pause.png';
            }
            else{
                clickedSong.src = preloadedSong.src;
                pastime.style.width = "0%";
                clickedSong.play();
                thisPlaybutton.src = '../static/Pause.png';
            }
        }
        else{
            if(preloadedSong.src == clickedSong.src){
                clickedSong.pause();
                thisPlaybutton.src = '../static/Play.png';
            }
            else{
                clickedSong.src = preloadedSong.src;
                pastime.style.width = "0%";
                clickedSong.play();
                thisPlaybutton.src = '../static/Pause.png';
            }
        }
        var interval = setInterval(function() {
        var widthline = Math.round(clickedSong.currentTime)/Math.round(clickedSong.duration) * 100;
    pastime.style.width = widthline + "%";
},1000);
        document.getElementById("pastime-" + musicName).style.display = 'inline-block';
    }
}

/* auto play */
function findTheIndex(src){
    return src == clickedSong.src;
}

var songsList = document.getElementsByClassName('musicSource');
var sourcesList = [];
var nextIndex = 0;
var arr = [];
for(i=0; i<songsList.length; i++){
    arr[i] = (function(para){return function(){sourcesList.push(songsList[i].getAttribute('value'));}}(i));
}

//sourcesList.findIndex(findTheIndex)
//document.getElementById('single-title').innerHTML = sourcesList.findIndex(findTheIndex) + 1;
/*
function findIndex(el){
  var i=1;
  while(el.previousSibling){
    el = el.previousSibling;
    el = el.previousSibling;
    if(el.nodeType === 1){
      i++;
    }
  }
  return i;
}

index = findIndex(currentBlockId);
*/
