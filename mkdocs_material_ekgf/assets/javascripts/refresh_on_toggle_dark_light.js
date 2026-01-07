(function () {
  // Global listener for palette changes
  document.addEventListener("change", function (event) {
    if (event.target && event.target.name === "__palette") {
      // Small delay to let Material for MkDocs process the change first
      setTimeout(function () {
        location.reload();
      }, 100);
    }
  });
})();
