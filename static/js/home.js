window.onload = function() {
  setTimeout(() => {
    const overlay = document.getElementById('startOverlay');
    const cover = document.getElementById('coverMain');
    if (overlay) overlay.classList.add('active');
    if (cover) cover.classList.add('active');
  }, 500);
};

$(document).ready(function () {
  const offset = 200;

  function updateReveal() {
    const windowHeight = $(window).height();
    const scrollTop = $(window).scrollTop();

    $('.reveal').each(function () {
      const $el = $(this);
      const top = $el.offset().top;
      const bottom = top + $el.outerHeight();

      if (top < scrollTop + windowHeight - offset && bottom > scrollTop) {
        $el.addClass('active');
      } else {
        $el.removeClass('active');
      }
    });
  }

  $(window).on('scroll resize', updateReveal);
  updateReveal(); // run once on load
});
