const hamburgerBtn = document.querySelector("#navbar-toggle-btn");
const sideNavbar = document.querySelector("#side-navbar");
const bgOverlay = document.querySelector("#bg-overlay");
let navbarOpen = false;
const toggleNavbar = () => {
  navbarOpen = !navbarOpen;
  sideNavbar.classList.toggle("translate-x-[16rem]");
  bgOverlay.classList.toggle("hidden");
};
hamburgerBtn.addEventListener("click", () => {
  toggleNavbar();
});
// Trap focus in modal - Inspired by https://hidde.blog/using-javascript-to-trap-focus-in-an-element/
const focusableEls = sideNavbar.querySelectorAll(
  'a[href]:not([disabled]), button:not([disabled]), textarea:not([disabled]), input[type="text"]:not([disabled]), input[type="radio"]:not([disabled]), input[type="checkbox"]:not([disabled]), select:not([disabled])'
);
const firstFocusableEl = focusableEls[0];
const lastFocusableEl = focusableEls[focusableEls.length - 1];
const KEYCODE_TAB = 9;
sideNavbar.addEventListener("keydown", (e) => {
  if (!navbarOpen) return;
  var isTabPressed = e.key === "Tab" || e.keyCode === KEYCODE_TAB;
  if (!isTabPressed) {
    return;
  }
  if (e.shiftKey) {
    /* shift + tab */ if (document.activeElement === firstFocusableEl) {
      lastFocusableEl.focus();
      e.preventDefault();
    }
  } /* tab */ else {
    if (document.activeElement === lastFocusableEl) {
      firstFocusableEl.focus();
      e.preventDefault();
    }
  }
});
// Prevent sidebar focus when closed
sideNavbar.addEventListener("focusin", (e) => {
  if (!navbarOpen) return hamburgerBtn.focus();
});
// Close side bar on escape and click outside
window.addEventListener("click", (e) => {
  if (!navbarOpen) return;
  if (!sideNavbar.contains(e.target) && !hamburgerBtn.contains(e.target)) toggleNavbar();
});
window.addEventListener("keydown", (e) => {
  if (!navbarOpen) return;
  if (e.key === "Escape") toggleNavbar();
});