(function () {
  "use strict";

  function restoreLazyBackgrounds() {
    document.querySelectorAll(".od-lazy-bg-image").forEach(function (node) {
      node.classList.remove("od-lazy-bg-image");
    });
  }

  function applyCssParallaxFallback() {
    var data = window.diviElementBackgroundParallaxData;
    if (!Array.isArray(data)) return;

    data.forEach(function (entry) {
      if (!entry || !Array.isArray(entry.data)) return;
      entry.data.forEach(function (item) {
        if (!item.enabled || !item.uniqueSelector) return;
        document.querySelectorAll(item.uniqueSelector).forEach(function (bg) {
          var imageUrl = item.imageUrl;
          if (imageUrl) {
            bg.style.backgroundImage = "url(" + imageUrl + ")";
          }
          bg.style.backgroundRepeat = "no-repeat";
          bg.style.backgroundSize = "cover";
          bg.style.backgroundPosition = "center top";
          bg.style.backgroundAttachment = "fixed";
          bg.style.height = "100%";
          bg.style.transform = "none";
        });
      });
    });
  }

  function initParallax() {
    restoreLazyBackgrounds();
    /* Divi trueParallax usa transform/height que vazam para seções acima no export estático. */
    applyCssParallaxFallback();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initParallax);
  } else {
    initParallax();
  }
})();
