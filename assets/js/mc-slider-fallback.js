(function () {
  "use strict";

  var AUTOPLAY_MS = 7000;

  function initSlider(slider) {
    if (slider.dataset.mcSlider) return;
    slider.dataset.mcSlider = "1";

    slider.classList.add("mc-slider-ready");
    slider.style.opacity = "1";

    var slidesWrap = slider.querySelector(".et_pb_slides");
    if (!slidesWrap) return;

    var slides = slidesWrap.querySelectorAll(":scope > .et_pb_slide");
    if (!slides.length) return;

    var current = 0;
    var timer = null;

    function showSlide(index) {
      if (index < 0) index = slides.length - 1;
      if (index >= slides.length) index = 0;
      current = index;

      slides.forEach(function (slide, i) {
        slide.classList.toggle("mc-active", i === current);
        slide.setAttribute("aria-hidden", i === current ? "false" : "true");
      });

      dots.forEach(function (dot, i) {
        dot.classList.toggle("mc-active", i === current);
        dot.setAttribute("aria-current", i === current ? "true" : "false");
      });
    }

    function next() {
      showSlide(current + 1);
    }

    function prev() {
      showSlide(current - 1);
    }

    function resetTimer() {
      if (timer) window.clearInterval(timer);
      if (slides.length > 1) {
        timer = window.setInterval(next, AUTOPLAY_MS);
      }
    }

    var controls = document.createElement("div");
    controls.className = "mc-slider-controls";
    controls.setAttribute("role", "group");
    controls.setAttribute("aria-label", "Navegação do carrossel");

    var prevBtn = document.createElement("button");
    prevBtn.type = "button";
    prevBtn.className = "mc-slider-arrow mc-slider-prev";
    prevBtn.setAttribute("aria-label", "Slide anterior");
    prevBtn.innerHTML = "&#10094;";

    var nextBtn = document.createElement("button");
    nextBtn.type = "button";
    nextBtn.className = "mc-slider-arrow mc-slider-next";
    nextBtn.setAttribute("aria-label", "Próximo slide");
    nextBtn.innerHTML = "&#10095;";

    var dotsWrap = document.createElement("div");
    dotsWrap.className = "mc-slider-dots";

    var dots = [];
    slides.forEach(function (_slide, i) {
      var dot = document.createElement("button");
      dot.type = "button";
      dot.className = "mc-slider-dot";
      dot.setAttribute("aria-label", "Ir para slide " + (i + 1));
      dot.addEventListener("click", function () {
        showSlide(i);
        resetTimer();
      });
      dotsWrap.appendChild(dot);
      dots.push(dot);
    });

    prevBtn.addEventListener("click", function () {
      prev();
      resetTimer();
    });
    nextBtn.addEventListener("click", function () {
      next();
      resetTimer();
    });

    controls.appendChild(prevBtn);
    controls.appendChild(dotsWrap);
    controls.appendChild(nextBtn);
    slider.appendChild(controls);

    slider.addEventListener("mouseenter", function () {
      if (timer) window.clearInterval(timer);
    });
    slider.addEventListener("mouseleave", resetTimer);

    showSlide(0);
    resetTimer();
  }

  function initAllSliders() {
    document.querySelectorAll(".et_pb_post_slider").forEach(initSlider);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAllSliders);
  } else {
    initAllSliders();
  }
})();
