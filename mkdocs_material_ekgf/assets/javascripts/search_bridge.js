(function () {
  // Bridge between our custom search box and Material's search modal
  // When user interacts with our search input, we open Material's search modal

  document.addEventListener("DOMContentLoaded", function () {
    var customSearchInput = document.querySelector(".ekgf-header-search__input");
    var materialSearchCheckbox = document.getElementById("__search");
    var materialSearchInput = document.querySelector(
      '[data-md-component="search-query"]'
    );

    if (!customSearchInput || !materialSearchCheckbox || !materialSearchInput) {
      return;
    }

    // When custom search input is focused or clicked, open Material's search
    customSearchInput.addEventListener("focus", function () {
      materialSearchCheckbox.checked = true;
      // Small delay to let the modal appear, then focus Material's input
      setTimeout(function () {
        materialSearchInput.focus();
      }, 50);
    });

    customSearchInput.addEventListener("click", function () {
      materialSearchCheckbox.checked = true;
      setTimeout(function () {
        materialSearchInput.focus();
      }, 50);
    });

    // If user starts typing while our input has focus, also forward to Material
    customSearchInput.addEventListener("keydown", function (e) {
      // Don't interfere with Tab or Escape
      if (e.key === "Tab" || e.key === "Escape") return;

      materialSearchCheckbox.checked = true;
      setTimeout(function () {
        materialSearchInput.focus();
        // If it was a character key, we need to dispatch it to Material's input
        if (e.key.length === 1) {
          materialSearchInput.value = e.key;
          materialSearchInput.dispatchEvent(new Event("input", { bubbles: true }));
        }
      }, 50);
    });
  });
})();
