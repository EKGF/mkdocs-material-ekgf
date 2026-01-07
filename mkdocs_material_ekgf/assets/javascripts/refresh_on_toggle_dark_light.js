(function () {
  console.log("EKGF Theme: Initializing robust palette listener...");

  // Listen for changes to the theme palette globally
  document.addEventListener("change", function (event) {
    // Check if the changed element is a theme palette radio button
    if (event.target && event.target.name === "__palette") {
      console.log("EKGF Theme: Palette change detected, reloading page...");
      // Small delay to let Material for MkDocs process the change and update local storage
      setTimeout(function () {
        location.reload();
      }, 100);
    }
  });
})();
