(function () {
  "use strict";

  function toggleContent(toggle) {
    return toggle.querySelector(":scope > .et_pb_toggle_content");
  }

  function closeToggle(toggle) {
    var content = toggleContent(toggle);
    if (!content || toggle.classList.contains("et_pb_toggle_close")) {
      return;
    }
    toggle.classList.remove("et_pb_toggle_open");
    toggle.classList.add("et_pb_toggle_close");
    content.style.display = "none";
  }

  function openToggle(toggle) {
    var content = toggleContent(toggle);
    if (!content || toggle.classList.contains("et_pb_toggle_open")) {
      return;
    }
    toggle.classList.remove("et_pb_toggle_close");
    toggle.classList.add("et_pb_toggle_open");
    content.style.display = "block";
  }

  function activateToggle(toggle) {
    var accordion = toggle.closest(".et_pb_accordion");
    if (
      accordion &&
      toggle.classList.contains("et_pb_accordion_item")
    ) {
      accordion.querySelectorAll(".et_pb_accordion_item.et_pb_toggle_open").forEach(function (item) {
        if (item !== toggle) {
          closeToggle(item);
        }
      });
      openToggle(toggle);
      return;
    }

    if (toggle.classList.contains("et_pb_toggle_open")) {
      closeToggle(toggle);
    } else {
      openToggle(toggle);
    }
  }

  function syncClosedState() {
    document.querySelectorAll(".et_pb_toggle.et_pb_toggle_close").forEach(function (toggle) {
      var content = toggleContent(toggle);
      if (content) {
        content.style.display = "none";
      }
    });
  }

  function bind() {
    if (document.body.dataset.mcToggleFallback) {
      return;
    }
    document.body.dataset.mcToggleFallback = "1";

    syncClosedState();

    document.body.addEventListener("click", function (event) {
      var title = event.target.closest(".et_pb_toggle_title, .et_fb_toggle_overlay");
      if (!title) {
        return;
      }

      var toggle = title.closest(".et_pb_toggle");
      if (!toggle || toggle.dataset.id) {
        return;
      }

      event.preventDefault();
      event.stopPropagation();
      activateToggle(toggle);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();
