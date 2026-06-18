(function () {
  "use strict";

  function replaceTag(el, tagName) {
    var replacement = document.createElement(tagName);
    for (var i = 0; i < el.attributes.length; i++) {
      var attr = el.attributes[i];
      replacement.setAttribute(attr.name, attr.value);
    }
    replacement.innerHTML = el.innerHTML;
    el.parentNode.replaceChild(replacement, el);
    return replacement;
  }

  function fixHeadings() {
    var hero = document.querySelector(".et_pb_heading_10 .et_pb_module_header");
    document.querySelectorAll("h1.et_pb_module_header").forEach(function (el) {
      if (hero && el === hero) {
        return;
      }
      replaceTag(el, "h2");
    });

    document.querySelectorAll("h5.et_pb_toggle_title").forEach(function (el) {
      replaceTag(el, "h3");
    });

    document.querySelectorAll(".et_pb_heading_2_tb_footer h1, .et_pb_heading_3_tb_footer h1").forEach(function (el) {
      replaceTag(el, "h2");
    });

    var footerPhone = document.querySelector(".et_pb_text_18_tb_footer h3");
    if (footerPhone) {
      replaceTag(footerPhone, "p");
    }
  }

  function fixLandmarks() {
    var main = document.getElementById("main-content");
    if (main && !main.getAttribute("role")) {
      main.setAttribute("role", "main");
    }
  }

  function fixButtons() {
    document.querySelectorAll(".et_pb_menu__search-button").forEach(function (btn) {
      if (!btn.getAttribute("aria-label")) {
        btn.setAttribute("aria-label", "Pesquisar");
      }
    });

    document.querySelectorAll(".et_pb_menu__close-search-button").forEach(function (btn) {
      if (!btn.getAttribute("aria-label")) {
        btn.setAttribute("aria-label", "Fechar pesquisa");
      }
    });

    document.querySelectorAll(".mobile_menu_bar").forEach(function (bar) {
      if (!bar.getAttribute("aria-label")) {
        bar.setAttribute("aria-label", "Abrir menu");
        bar.setAttribute("role", "button");
        bar.setAttribute("tabindex", "0");
      }
    });
  }

  function fixImages() {
    document.querySelectorAll(".et_pb_image_0_tb_header img").forEach(function (img) {
      if (!img.getAttribute("alt")) {
        img.setAttribute("alt", "Mentes Criativas");
      }
    });
  }

  function init() {
    fixLandmarks();
    fixButtons();
    fixImages();
    fixHeadings();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
