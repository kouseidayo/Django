const randomIndex = Math.floor(Math.random() * 3);

let imageSrc;

if (randomIndex === 0) {
  imageSrc = "../../../media/イッヌ.png";
} else if (randomIndex === 1) {
  imageSrc = "../../../media/魚.png";
} else {
  imageSrc = "../../../media/鳥.png";
}

const image = document.getElementById("image");
image.src = imageSrc;