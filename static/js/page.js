
document.addEventListener("DOMContentLoaded", () => {
  const img = document.querySelector(".cover-img");
  const imageWrap = document.querySelector(".cover .image");
  const footer = document.querySelector(".footer");

  if (!img || !footer || !imageWrap) return;

  function checkPosition() {
    const footerTop = footer.getBoundingClientRect().top + window.scrollY;
    const imgHeight = window.innerHeight; // since we force image to 100vh

    // When the viewport top has scrolled so far that the fixed image would hit footer:
    const stopPoint = footerTop - imgHeight;

    if (window.scrollY >= stopPoint) {
      img.classList.add("relative");
    } else {
      img.classList.remove("relative");
    }
  }

  window.addEventListener("scroll", checkPosition, { passive: true });
  window.addEventListener("resize", checkPosition);
  checkPosition();
});