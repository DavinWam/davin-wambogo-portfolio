function openModal() {
  document.getElementById("my-modal").style.display = "flex";
  var i;
  var slides = document.getElementsByClassName("myslides");
  for (i = 0; i < slides.length; i++) {
    print(i);
    slides[i].style.display = "none"; // Hide all slides
  }
}
 
function closeModal() {
  document.getElementById("my-modal").style.display = "none";
}

var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex -= n); // Reverse order when n is positive
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("my-slides");
  if (n > slides.length) { slideIndex = 1; } // Loop to the first slide
  if (n < 1) { slideIndex = slides.length; } // Loop to the last slide
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none"; // Hide all slides
  }
  slides[slideIndex - 1].style.display = "block"; // Show the current slide
}
