// Always open at the top of the page (phones otherwise jump back to where you last were),
// unless the link points at a section like #quote
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
window.addEventListener("load", function () {
  if (!location.hash) window.scrollTo(0, 0);
});

// Loading screen: stays up until its animation has fully played (about 2.3s from when it first
// appears on screen) and the page is ready, then slides away. Never longer than ~5s in total.
const root = document.documentElement;
if (root.classList.contains("is-loading")) {
  const calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const playTime = calm ? 500 : 2300;
  let shownAt = null;
  let pageReady = false;
  let done = false;

  const hide = function () {
    if (done) return;
    done = true;
    root.classList.add("is-loaded");
    try { sessionStorage.setItem("cti-intro", "1"); } catch (e) {}
    setTimeout(function () { root.classList.remove("is-loading", "is-loaded"); }, 850);
  };
  const tryHide = function () {
    if (shownAt === null || !pageReady) return;
    setTimeout(hide, Math.max(0, playTime - (performance.now() - shownAt)));
  };

  // The animation starts on the first frame drawn, so start the clock there
  requestAnimationFrame(function () {
    shownAt = performance.now();
    tryHide();
  });
  if (document.readyState === "complete") pageReady = true;
  else window.addEventListener("load", function () { pageReady = true; tryHide(); });
  setTimeout(hide, Math.max(0, 5000 - performance.now()));
}

// Menu and "Free Quote" links: scroll to the section, then double-check we really landed on it.
// (If anything above it changed size while scrolling, jump the last bit so it's exact.)
const headerOffset = function () {
  return document.querySelector(".site-header").offsetHeight + 8;
};
const targetTop = function (el) {
  return el.getBoundingClientRect().top + window.scrollY - headerOffset();
};
document.querySelectorAll('a[href^="#"]').forEach(function (link) {
  const id = link.getAttribute("href");
  if (id.length < 2) return;
  link.addEventListener("click", function (event) {
    const target = document.querySelector(id);
    if (!target) return;
    event.preventDefault();
    history.pushState(null, "", id);
    window.scrollTo({ top: targetTop(target), behavior: "smooth" });

    let checks = 0;
    const settle = function () {
      const off = Math.abs(target.getBoundingClientRect().top - headerOffset());
      if (off > 4) window.scrollTo({ top: targetTop(target), behavior: "instant" });
      if (++checks < 3) setTimeout(settle, 400);
    };
    setTimeout(settle, 900);
  });
});

// Keep the footer year current
document.getElementById("year").textContent = new Date().getFullYear();

// Quote form: sends the request straight to the business Gmail through FormSubmit (free).
const form = document.getElementById("quote-form");
const statusText = document.getElementById("form-status");
const success = document.getElementById("form-success");
const button = form.querySelector(".quote-submit");
const buttonText = button.querySelector(".label-text");

form.addEventListener("submit", async function (event) {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form));

  data._subject = "New quote request: " + data.project + " (" + data.name + ")";
  data._template = "table";
  data._captcha = "false";
  if (data.email) data._replyto = data.email;

  button.disabled = true;
  buttonText.textContent = "Sending…";
  statusText.className = "form-status";
  statusText.textContent = "";

  try {
    const response = await fetch("https://formsubmit.co/ajax/agcustomtileinteriors@gmail.com", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data),
    });
    // FormSubmit answers 200 even when it didn't send, so check its "success" flag too
    const result = await response.json();
    if (!response.ok || String(result.success) !== "true") throw new Error(result.message || "Request failed");

    form.reset();
    form.hidden = true;
    success.hidden = false;
    success.scrollIntoView({ behavior: "smooth", block: "center" });
  } catch (error) {
    statusText.classList.add("is-error");
    statusText.innerHTML = 'Sorry, something went wrong. Please call us at <a href="tel:+16129917000">612-991-7000</a>.';
  } finally {
    button.disabled = false;
    buttonText.textContent = "Get My Free Quote";
  }
});

document.getElementById("send-another").addEventListener("click", function () {
  success.hidden = true;
  form.hidden = false;
});
