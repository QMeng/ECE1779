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
        document.getElementById('single-title').innerHTML = 'No music here.';
        document.getElementById('single-artist').innerHTML = 'Unknown';
        document.getElementById('shareList').style.display = 'none';
        document.getElementById('stopSharing').style.display = 'none';
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
var currentBlockEl = '';

for (i=0; i<songBlocks.length; i++){
    songBlocks[i].onclick = function(){
        var musicName = this.id;
        thisPlaybutton = document.getElementById("playbutton-" + musicName);
        var pastimes = document.getElementsByClassName('pastime');
        currentBlockEl = this;
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

var songsList = document.getElementsByClassName('musicSource');
var nextIndex = 0;
var arr = [];


clickedSong.onended = function(){
    if((currentBlockEl.nextSibling).nextSibling){
            (currentBlockEl.nextSibling).nextSibling.click();
        }
}

getAverageRGBFromImgsrc('https://ece1779-images-remi.s3.amazonaws.com/2.jpeg?AWSAccessKeyId=AKIAJXRND7TNNOWKC4MA&Signature=%2FjTZCWgFI6v8xxwo3DXd6IkxgwI%3D&Expires=1543889213').then(function(rgb){
  console.log(rgb);
  document.getElementById('mytest').style.backgroundColor = 'rgb('+rgb.r+','+rgb.g+','+rgb.b+')';
});


function getAverageRGBFromImgsrc(imgSrc){
  return new Promise(function(resolve, reject){
    var imgEl = document.createElement('img');
    imgEl.onload = function(e) {
      // context.drawImage(imgEl, 0, 0, canvas.width, canvas.height);
      // var url = canvas.toDataURL(); // Read succeeds, canvas won't be dirty.
      var rgb = getAverageRGB(imgEl);
      resolve(rgb);
    };
    imgEl.crossOrigin = '';
    imgEl.src = imgSrc;
  });
}

function getAverageRGB(imgEl) {

  var blockSize = 5, // only visit every 5 pixels
      defaultRGB = {r:255,g:255,b:255}, // for non-supporting envs
      canvas = document.createElement('canvas'),
      context = canvas.getContext && canvas.getContext('2d'),
      data, width, height,
      i = -4,
      length,
      rgb = {r:0,g:0,b:0},
      count = 0;

  if (!context) {
    return defaultRGB;
  }

  height = canvas.height = imgEl.naturalHeight || imgEl.offsetHeight || imgEl.height;
  width = canvas.width = imgEl.naturalWidth || imgEl.offsetWidth || imgEl.width;

  context.drawImage(imgEl, 0, 0);

  try {
    data = context.getImageData(0, 0, width, height);
  } catch(e) {
    return defaultRGB;
  }

  length = data.data.length;

  while ( (i += blockSize * 4) < length ) {
    ++count;
    rgb.r += data.data[i];
    rgb.g += data.data[i+1];
    rgb.b += data.data[i+2];
  }

  // ~~ used to floor values
  rgb.r = ~~(rgb.r/count);
  rgb.g = ~~(rgb.g/count);
  rgb.b = ~~(rgb.b/count);

  return rgb;
}


document.getElementById('close_button').onclick = function(){
    document.getElementById('wrap').style.display = 'none';
}
