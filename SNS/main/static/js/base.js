window.addEventListener("scroll", function(){
  let scrollPosition = window.pageYOffset;
  let bg = document.querySelector("body");
  bg.style.backgroundPositionY = scrollPosition * 0.3 + "px";
});