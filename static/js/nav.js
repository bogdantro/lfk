
window.addEventListener("scroll", function(){
    const navbar = document.getElementById('mobileNav');
    navbar.classList.toggle("sticky", window.scrollY > 40)
  })


  window.addEventListener("scroll", function(){
    const navbar = document.getElementById('desNav');
    navbar.classList.toggle("sticky", window.scrollY > 1)
})


document.addEventListener("DOMContentLoaded", function () {

  const hasYellowCover = document.querySelector(".cover.yellow");
  if (!hasYellowCover) return;

  const desktopNav = document.getElementById("desNav");
  const mobileNav = document.getElementById("mobileNav");

  if (desktopNav) desktopNav.classList.add("yellow-nav");
  if (mobileNav) mobileNav.classList.add("yellow-nav");

});



/////////// MOBILE JAVASCRIPT
// MENU
function menu(){
  const sidebar = document.getElementById('sidebar');
  const navbar = document.getElementById('mobileNav');
  const hamburger = document.getElementById('hamburger');

  const dropdown = document.getElementById('sidebarServDrop');

  const body = document.getElementsByTagName('body')[0];

  if (window.getComputedStyle(sidebar,null).getPropertyValue("opacity") == '0'){
    navbar.classList.add('menu')  
    hamburger.classList.add('click')  
    sidebar.classList.add('active')
    body.style.overflowY = 'hidden';
    dropdown.classList.remove('active')
  } else{
    navbar.classList.remove('menu') 
    hamburger.classList.remove('click')  
    sidebar.classList.remove('active')
  }  
};

