document.addEventListener("DOMContentLoaded", () => {

const images = document.querySelectorAll(".cover-img");
const footer = document.querySelector(".footer");

if(!images.length || !footer) return;

function checkPosition(){

const footerTop = footer.getBoundingClientRect().top + window.scrollY;
const imgHeight = window.innerHeight;

const stopPoint = footerTop - imgHeight;

images.forEach(img => {

if(window.scrollY >= stopPoint){
img.classList.add("relative");
}else{
img.classList.remove("relative");
}

});

}

window.addEventListener("scroll", checkPosition, { passive:true });
window.addEventListener("resize", checkPosition);

checkPosition();

});