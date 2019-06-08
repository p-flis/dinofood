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
