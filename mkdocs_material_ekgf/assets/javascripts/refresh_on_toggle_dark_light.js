(function () {
  // Listen for any change event on the document
  document.addEventListener("change", function (event) {
    // Check if the changed element is a theme palette radio button
    if (event.target && event.target.name === "__palette") {
      // Small delay to let Material for MkDocs process the change first
      setTimeout(function () {
        location.reload();
      }, 100);
    }
  });
})();
