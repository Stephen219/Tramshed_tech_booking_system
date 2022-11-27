import { createFocusTrap } from "focus-trap";
const hamburgerBtn = document.querySelector("#navbar-toggle-btn");
const sideNavbar = document.querySelector("#side-navbar");
const bgOverlay = document.querySelector("#bg-overlay");
let navbarOpen = false;
const trap = createFocusTrap(sideNavbar);
const toggleNavbar = () => {
  navbarOpen = !navbarOpen;
  if (navbarOpen) trap.activate();
  else trap.deactivate();
  sideNavbar.classList.toggle("translate-x-0");
  bgOverlay.classList.toggle("hidden");
};
hamburgerBtn.addEventListener("click", () => {
  toggleNavbar();
});
window.addEventListener("click", (e) => {
  if (!navbarOpen) return;
  if (!sideNavbar.contains(e.target) && !hamburgerBtn.contains(e.target)) toggleNavbar();
});
