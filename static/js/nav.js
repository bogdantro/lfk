
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

document.addEventListener("DOMContentLoaded", function () {

  const triggers = document.querySelectorAll("#sidebar .mob-dd-trigger");

  triggers.forEach(btn => {

    btn.addEventListener("click", function (e) {

      e.preventDefault();

      const targetId = btn.dataset.target;
      const panel = document.getElementById(targetId);
      if (!panel) return;

      const isSub = btn.classList.contains("sub");
      const isOpen = panel.classList.contains("open");

      // MAIN DROPDOWNS (Sport / Marked / etc)
      if (!isSub) {

        document.querySelectorAll("#sidebar > .mob-dd").forEach(dd => {
          dd.classList.remove("open");
        });

        document.querySelectorAll("#sidebar > .mob-dd-trigger").forEach(tr => {
          tr.classList.remove("open");
        });

      }

      // SUB DROPDOWNS (Lag)
      if (isSub) {

        const parent = btn.closest(".mob-dd");

        parent.querySelectorAll(".mob-dd.sub").forEach(dd => {
          dd.classList.remove("open");
        });

        parent.querySelectorAll(".mob-dd-trigger.sub").forEach(tr => {
          tr.classList.remove("open");
        });

      }

      if (!isOpen) {
        panel.classList.add("open");
        btn.classList.add("open");
      }

    });

  });

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
    navbar.classList.add('menu');
    hamburger.classList.add('click');
    sidebar.classList.add('active');
    body.style.overflowY = 'hidden';
    if (dropdown) dropdown.classList.remove('active');
  } else{
    navbar.classList.remove('menu');
    hamburger.classList.remove('click');
    sidebar.classList.remove('active');
    body.style.overflowY = 'auto';
  }
};

