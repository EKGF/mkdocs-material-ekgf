(function () {
  console.log("EKGF Theme: Initializing robust palette listener...");

  function setupListener() {
    // We listen for clicks on any element
    document.addEventListener("click", function (event) {
      // Find the closest label that points to a palette entry
      var label = event.target.closest("label.md-header__button");
      if (
        label &&
        label.getAttribute("for") &&
        label.getAttribute("for").startsWith("__palette_")
      ) {
        console.log("EKGF Theme: Palette label clicked, preparing reload...");
        
        // We wait for the underlying radio button to change and for Material to process it
        setTimeout(function () {
          console.log("EKGF Theme: Reloading now...");
          location.reload();
        }, 200);
      }
    });

    // Also keep the change listener as a fallback
    document.addEventListener("change", function (event) {
      if (event.target && event.target.name === "__palette") {
        console.log("EKGF Theme: Palette radio changed, preparing reload...");
        setTimeout(function () {
          location.reload();
        }, 200);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupListener);
  } else {
    setupListener();
  }
})();
