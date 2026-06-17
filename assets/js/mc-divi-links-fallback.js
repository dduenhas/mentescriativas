(function () {
  "use strict";

  function decodeUrl(url) {
    return url.replace(/&#91;/g, "[").replace(/&#93;/g, "]");
  }

  function navigate(url, target) {
    url = decodeUrl(url);
    if (target === "_blank") {
      window.open(url, "_blank", "noopener,noreferrer");
    } else {
      window.location.href = url;
    }
  }

  function isExcludedClickTarget(el) {
    var selectors = [
      ".et_pb_toggle_title",
      ".mejs-container",
      ".et_pb_contact_field input",
      ".et_pb_contact_field textarea",
      ".et_pb_contact_field_checkbox",
      ".et_pb_contact_field_radio",
      ".et_pb_contact_captcha",
      ".et_pb_tabs_controls a",
      ".flex-control-nav",
      ".et_pb_menu__search-button",
      ".et_pb_menu__close-search-button",
      ".et_pb_menu__search-container",
      ".et_pb_fullwidth_header_scroll",
    ];
    for (var i = 0; i < selectors.length; i++) {
      if (el.closest(selectors[i])) return true;
    }
    return false;
  }

  function collectLinkData() {
    var items = [];
    if (window.diviElementLinkData) {
      items = items.concat(window.diviElementLinkData);
    }
    if (window.et_link_options_data) {
      items = items.concat(window.et_link_options_data);
    }
    return items;
  }

  function initMcDiviLinks() {
    var items = collectLinkData();
    if (!items.length) return;

    items.forEach(function (item) {
      if (!item.class || !item.url || !item.target) return;

      document.querySelectorAll("." + item.class).forEach(function (node) {
        if (node.dataset.mcDiviLink) return;
        node.dataset.mcDiviLink = "1";
        node.style.cursor = "pointer";

        node.addEventListener("click", function (event) {
          if (event.target.closest("a, button")) return;
          if (
            event.target !== event.currentTarget &&
            isExcludedClickTarget(event.target)
          ) {
            return;
          }
          event.stopPropagation();
          navigate(item.url, item.target);
        });
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMcDiviLinks);
  } else {
    initMcDiviLinks();
  }
})();
