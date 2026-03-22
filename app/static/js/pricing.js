// Marquee
const marquee = document.querySelector('.marquee span');
if(marquee){
  let pos = 100;
  setInterval(() => {
    pos--;
    if(pos < -marquee.offsetWidth) pos = 100;
    marquee.style.transform = `translateX(${pos}px)`;
  }, 20);
}

// Carousel (basic)
let idx = 0;
const slides = document.querySelectorAll('.carousel img');
if(slides.length > 0){
  setInterval(()=>{
    slides.forEach((s,i)=>s.style.display = (i==idx) ? 'block' : 'none');
    idx = (idx+1) % slides.length;
  }, 3000);
}
