function checkStars(starId){
  var stars = document.getElementsByClassName('star');
  for (i = 0; i < stars.length; i++) {
    (stars[i]).classList.remove('selected');
  }
  for (i = 0; i < starId; i++) {
    (stars[i]).classList.add('selected');
  }
}

function hoverStars(starId){
  var stars = document.getElementsByClassName('star');
  for (i = 0; i < stars.length; i++) {
    if(i<starId) {
      (stars[i]).classList.add('hover');
    }
    else {
      (stars[i]).classList.remove('hover');
    }
  }
}

function clearHoverStars(starId){
  var stars = document.getElementsByClassName('star');
  for (i = 0; i < stars.length; i++) {
    (stars[i]).classList.remove('hover');
  }
}

function checkFavourite(starId){
  var heart = document.getElementsByClassName('heart')[0];
  if(heart.classList.contains('selected'))
    heart.classList.remove('selected');
  else
    heart.classList.add('selected');
}

function hoverFavourite(starId){
  var heart = document.getElementsByClassName('heart')[0];
  heart.classList.add('hover');
}

function clearHoverFavourite(starId){
  var heart = document.getElementsByClassName('heart')[0];
  heart.classList.remove('hover');
}
