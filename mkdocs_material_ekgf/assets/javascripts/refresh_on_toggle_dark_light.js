(function () {
  // Listen for changes to the theme palette globally using event delegation
  // This works regardless of when the script loads or when elements are added to the DOM
  document.addEventListener("change", function (event) {
    // Check if the changed element is a theme palette radio button
    if (event.target && event.target.name === "__palette") {
      // Small delay to let Material for MkDocs process the change and update local storage
      setTimeout(function () {
        location.reload();
      }, 100);
    }
  });
})();
