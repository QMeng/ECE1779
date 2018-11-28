/* showing the first picture in the playlist */
var pics = document.getElementsByClassName('pics');
function showFirstPic(){
    if (pics.length != 0){
        document.getElementById('pic01').src = '';
        document.getElementById('pic01').src = pics[0].getAttribute('value');
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
testdurationSong = new Audio();

for (i=0; i<songBlocks.length; i++){
    document.getElementById("songtime-" + songBlocks[i].id).innerHTML = '0' + ':0' + '0';
    songBlocks[i].onclick = function(){
        var musicName = this.id;
        thisPlaybutton = document.getElementById("playbutton-" + musicName);
        //thisPlaybutton.style.display= 'inline-block';
        var pastimes = document.getElementsByClassName('pastime');
        for (i=0; i<pastimes.length; i++){
            pastimes[i].style.display = 'none';
        }
        preloadedSong.src = document.getElementById("music-" + musicName).getAttribute("value");
        document.getElementById('pic01').src = document.getElementById("image-" + musicName).getAttribute("value");
        var pastime = document.getElementById("pastime-" + musicName);
        //testing = test;
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

/* control bar */


//setInterval(playNext(preloadedSong, songsList, clickedSong),1000);
/* check playList */

/*
function getPlayList(preloadedSong, songsList){
    var songNames = new Array();
    var currentIndex = -1;
    for (i=0; i<songsList.length; i++){
        songNames.push(songsList[i].getAttribute('value'));
    }
    currentIndex = songNames.indexOf(preloadedSong.src);
    if (currentIndex +1 >= songNames.length){
        return [];
    }
    else{
        return songNames.slice(currentIndex+1,songNames.length);
    }
}

function playNext(preloadedSong, songsList, clickedSong){
    var songNames = new Array();
    var currentIndex = -1;
    var playList = getPlayList(preloadedSong, songsList)
    if(clickedSong.paused){
        if(clickedSong.ended){
            preloadedSong.src = playList[0];
            clickedSong.src = playList[0];
            }
    }
    return clickedSong.src;
}
*/
var songsList = document.getElementsByClassName('musicSource');

clickedSong.addEventListener('ended',function(songsList){
    var songNames = new Array();
    var currentIndex = -1;
    var songNames = new Array();
    var currentIndex = -1;
    var playList = [];
    for (i=0; i<songsList.length; i++){
        songNames.push(songsList[i].getAttribute('value'));
    }
    currentIndex = songNames.indexOf(preloadedSong.src);
    if (currentIndex +1 < songNames.length){
        if(clickedSong.paused){
        if(clickedSong.ended){
            preloadedSong.src = playList[0];
            clickedSong.src = playList[0];
            }
    }
        //playList = songNames.slice(currentIndex+1,songNames.length);
    }
    return clickedSong.src;
    });

function playNext(preloadedSong, songsList, clickedSong){
    var songNames = new Array();
    var currentIndex = -1;
    var songNames = new Array();
    var currentIndex = -1;
    var playList = [];
    for (i=0; i<songsList.length; i++){
        songNames.push(songsList[i].getAttribute('value'));
    }
    currentIndex = songNames.indexOf(preloadedSong.src);
    if (currentIndex +1 < songNames.length){
        if(clickedSong.paused){
        if(clickedSong.ended){
            preloadedSong.src = playList[0];
            clickedSong.src = playList[0];
            }
    }
        //playList = songNames.slice(currentIndex+1,songNames.length);
    }
    return clickedSong.src;
}
//setInterval(playNext(preloadedSong, songsList, clickedSong, allBlocks),100);

