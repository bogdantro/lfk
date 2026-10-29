
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

// Over the promotion hero the desktop nav is see-through with white links;
// the existing "sticky" class brings the white background back on scroll
document.addEventListener("DOMContentLoaded", function () {

  const desktopNav = document.getElementById("desNav");
  if (!desktopNav || !document.getElementById("promoHero")) return;

  desktopNav.classList.add("over-hero");
  // A reload halfway down the page keeps its scroll position, so set it now too
  desktopNav.classList.toggle("sticky", window.scrollY > 1);

});

document.addEventListener("DOMContentLoaded", function () {

  const sheet = document.getElementById("sidebar");
  if (!sheet) return;

  const sections = sheet.querySelectorAll(".mm-section");

  function setOpen(section, open) {
    const btn = section.querySelector(".mm-trigger");
    section.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  // Accordion: one section open at a time
  sections.forEach(function (section) {
    section.querySelector(".mm-trigger").addEventListener("click", function () {
      const willOpen = !section.classList.contains("open");
      sections.forEach(function (s) { setOpen(s, false); });
      if (willOpen) setOpen(section, true);
    });
  });

  // Highlight the current page and open its section
  const here = window.location.pathname.replace(/\/+$/, "") || "/";
  sheet.querySelectorAll("a[href^='/']").forEach(function (link) {
    const path = link.getAttribute("href").split("#")[0].replace(/\/+$/, "") || "/";
    if (path === here && path !== "/") {
      link.classList.add("is-current");
      link.setAttribute("aria-current", "page");
      const section = link.closest(".mm-section");
      if (section) setOpen(section, true);
    }
  });

  // Close when following an in-page link (e.g. /#stampaShopHome)
  sheet.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      if (sheet.classList.contains("active")) menu();
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && sheet.classList.contains("active")) menu();
  });

  const hamburger = document.getElementById("hamburger");
  if (hamburger) {
    hamburger.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); menu(); }
    });
  }

});

/////////// MOBILE JAVASCRIPT
// MENU
function menu(){
  const sheet = document.getElementById('sidebar');
  const navbar = document.getElementById('mobileNav');
  const hamburger = document.getElementById('hamburger');
  const root = document.documentElement;
  if (!sheet) return;

  const open = !sheet.classList.contains('active');

  sheet.classList.toggle('active', open);
  sheet.setAttribute('aria-hidden', open ? 'false' : 'true');
  if (navbar) navbar.classList.toggle('menu', open);
  if (hamburger) {
    hamburger.classList.toggle('click', open);
    hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  // Lock page scroll behind the menu
  root.classList.toggle('mm-locked', open);
  document.body.classList.toggle('mm-locked', open);

  if (open) {
    const close = document.getElementById('mmClose');
    if (close) setTimeout(function () { close.focus({ preventScroll: true }); }, 50);
  } else if (hamburger) {
    hamburger.focus({ preventScroll: true });
  }
};

/////////// DESKTOP DROPDOWNS
document.addEventListener("DOMContentLoaded", function () {

  const items = document.querySelectorAll("#desNav .nav-item");
  if (!items.length) return;

  const here = window.location.pathname.replace(/\/+$/, "") || "/";

  items.forEach(function (item) {
    const trigger = item.querySelector(".nav-trigger");
    if (!trigger) return;

    function setExpanded(open) {
      trigger.setAttribute("aria-expanded", open ? "true" : "false");
    }

    item.addEventListener("mouseenter", function () { item.classList.remove("is-dismissed"); setExpanded(true); });
    item.addEventListener("mouseleave", function () { item.classList.remove("is-dismissed"); setExpanded(false); });
    item.addEventListener("focusin", function () { item.classList.remove("is-dismissed"); setExpanded(true); });
    item.addEventListener("focusout", function (e) {
      if (!item.contains(e.relatedTarget)) setExpanded(false);
    });

    // Click toggles for touch screens / keyboard users
    trigger.addEventListener("click", function () {
      const open = item.classList.toggle("is-open");
      if (!open) item.classList.add("is-dismissed");
      setExpanded(open);
    });

    item.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        item.classList.remove("is-open");
        item.classList.add("is-dismissed");
        setExpanded(false);
        trigger.focus();
      }
    });

    // Mark the section of the current page
    item.querySelectorAll(".dropdown a[href^='/']").forEach(function (link) {
      const path = link.getAttribute("href").split("#")[0].replace(/\/+$/, "") || "/";
      if (path === here && path !== "/") {
        link.classList.add("is-current");
        link.setAttribute("aria-current", "page");
        item.classList.add("is-current");
      }
    });
  });

  // Close click-opened panels when clicking elsewhere
  document.addEventListener("click", function (e) {
    items.forEach(function (item) {
      if (!item.contains(e.target)) item.classList.remove("is-open");
    });
  });

});
