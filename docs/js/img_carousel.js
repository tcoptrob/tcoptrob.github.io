var keepTime = 2000;

function updateCarousel(img) {
  if (img.carouselRunning) {
    let outstyle = img.carousel[img.carouselIndex % img.carousel.length].style;
    outstyle.visibility = 'hidden';
    outstyle.opacity = 0;
    img.carouselIndex = (img.carouselIndex + 1) % img.carousel.length;
    let instyle = img.carousel[img.carouselIndex % img.carousel.length].style;
    instyle.visibility = 'visible';
    instyle.opacity = 1;
    instyle.margin = "margin: 0 300px"
    // instyle.position = 'absolute';
  }
  setTimeout(updateCarousel, keepTime, img);
}

function setCarouselEvents(img) {
  img.style.visibility = 'hidden';
  img.style.transition = 'opacity 1.3s, visibility 1.3s';
//   img.style.position = 'absolute';
  img.addEventListener(
      'mouseover', function(e) { this.carousel[0].carouselRunning = false; });
  img.addEventListener(
      'mouseout', function(e) { this.carousel[0].carouselRunning = true; });
}

function setCarousel(img) {
  img.carouselRunning = true;
  setCarouselEvents(img);
  img.carouselIndex = 0;
  setTimeout(updateCarousel, 1, img);
}

// fist we need to ask DOM for all p > img tags
let imgs = document.querySelectorAll('DIV > IMG');
// let imgs = document.getElementById('carousel_container').getElementsByTagName('img')
for (let i = 1; i < imgs.length; i++) {
  console.log(imgs[i].src)
  if (imgs[i].className != "carousel")
    continue;
  let h = imgs[i].naturalHeight;
  let w = imgs[i].naturalWidth;
  let pe = imgs[i].previousElementSibling;

  if (!pe) {
    continue;
  }
  if (pe.nodeName != "IMG") {
    continue;
  }
  let sh = pe.naturalHeight;
  let sw = pe.naturalWidth;
  if (sw != w || sh != h) {
    continue;
  }
  if (imgs[i].carousel) {
    continue;
  }
  if (!pe.carousel) {
    pe.carousel = [ pe ];
    setCarousel(pe);
  }
  pe.carousel.push(imgs[i]);
  imgs[i].carousel = pe.carousel;
  setCarouselEvents(imgs[i]);
//   // set parent size
//   pe.parentElement.style.minWidth = "calc(" + sw + "px + 2em)";
//   pe.parentElement.style.minHeight = "calc(" + sh + "px + 2em)";
}
