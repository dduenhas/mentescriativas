(function () {
  "use strict";

  if (typeof window.et_pb_box_shadow_apply_overlay !== "function") {
    window.et_pb_box_shadow_apply_overlay = function () {};
  }

  function ensureDiviModulesInit() {
    var jq = window.jQuery;
    if (!jq || typeof jq.fn !== "object" || typeof jq.fn.on !== "function") {
      return;
    }
    jq(function () {
      jq(window).trigger("et_pb_init_modules");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ensureDiviModulesInit);
  } else {
    ensureDiviModulesInit();
  }
})();
