window.addEventListener("scroll", function(){
  let scrollPosition = window.pageYOffset;
  let bg = document.querySelector("body");
  bg.style.backgroundPositionY = scrollPosition * 0.3 + "px";
});


function handleButtonClick() {
const nav = document.getElementById('nav-left');
if (nav.style.display === 'flex'){
nav.style.display = 'none';
} else{
nav.style.display = 'flex';
}
}

