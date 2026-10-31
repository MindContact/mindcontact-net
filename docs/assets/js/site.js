// Menu: a <details> toggle on phones and tablets, always open as an inline nav on desktop.
(function () {
  var menu = document.querySelector(".menu");
  if (!menu) return;
  document.documentElement.classList.add("js");
  var desktop = window.matchMedia("(min-width: 64rem)");
  function sync() { menu.open = desktop.matches; }
  sync();
  desktop.addEventListener("change", sync);
  menu.querySelectorAll("nav a").forEach(function (a) {
    a.addEventListener("click", function () { if (!desktop.matches) menu.open = false; });
  });
})();
