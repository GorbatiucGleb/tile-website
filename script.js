// Custom Tile Interiors — page behavior.
// Each feature is set up separately, so if one ever breaks the others keep working.

const root = document.documentElement;

// Tracks whether the visitor has started scrolling or tapping on their own
let userMoved = false;
["wheel", "touchstart", "keydown"].forEach(function (type) {
  window.addEventListener(type, function () { userMoved = true; }, { passive: true });
});

function safely(name, setup) {
  try { setup(); } catch (error) { console.error("[" + name + "]", error); }
}

// ---------- Open at the top ----------
// Phones otherwise jump back to wherever you were last time.
// A section link like /#quote is only followed when it comes from our own pages (the service
// pages' Free Quote buttons). A link someone texted with #services on the end opens at the top.
safely("open at top", function () {
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  let fromOurSite = false;
  try { fromOurSite = !!document.referrer && new URL(document.referrer).host === location.host; } catch (e) {}
  if (location.hash && !fromOurSite) history.replaceState(null, "", location.pathname + location.search);
  window.addEventListener("load", function () {
    if (!location.hash && !userMoved) window.scrollTo(0, 0);
  });
});

// ---------- Loading screen ----------
// Stays up until its animation has fully played (about 2.3s from when it first appears)
// and the page is ready, then slides away. Never longer than ~5s in total.
safely("loading screen", function () {
  if (!root.classList.contains("is-loading")) return;
  const calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const playTime = calm ? 500 : 2300;
  let shownAt = null;
  let pageReady = document.readyState === "complete";
  let done = false;

  const hide = function () {
    if (done) return;
    done = true;
    root.classList.add("is-loaded");
    try { sessionStorage.setItem("cti-intro", "1"); } catch (e) {}
    setTimeout(function () {
      root.classList.remove("is-loading", "is-loaded");
      document.dispatchEvent(new Event("cti:intro-done"));
    }, 850);
  };
  const tryHide = function () {
    if (shownAt === null || !pageReady) return;
    setTimeout(hide, Math.max(0, playTime - (performance.now() - shownAt)));
  };

  // The animation starts on the first frame drawn, so start the clock there
  requestAnimationFrame(function () { shownAt = performance.now(); tryHide(); });
  if (!pageReady) window.addEventListener("load", function () { pageReady = true; tryHide(); });
  setTimeout(hide, Math.max(0, 5000 - performance.now()));
});

// ---------- Menu and "Free Quote" links ----------
// Smooth-scrolls to the section. Once the scrolling stops, it checks it landed exactly right
// and fixes the last bit if not. A new tap, or the visitor scrolling themselves, cancels any
// check that's still waiting, so taps never fight each other.
safely("section links", function () {
  const header = document.querySelector(".site-header");
  // Leave room for the menu only when it's stuck to the top of the screen
  const headerOffset = function () {
    const stuck = header && getComputedStyle(header).position === "sticky";
    return (stuck ? header.offsetHeight : 0) + 8;
  };
  const topOf = function (el) { return el.getBoundingClientRect().top + window.scrollY - headerOffset(); };

  let current = null;   // the section we're heading to right now
  let idleTimer = null;

  const stop = function () { current = null; clearTimeout(idleTimer); };
  const checkLanding = function () {
    if (!current) return;
    const target = current;
    stop();
    const off = Math.abs(target.getBoundingClientRect().top - headerOffset());
    const atBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2;
    if (off > 4 && !atBottom) window.scrollTo({ top: topOf(target), behavior: "instant" });
  };
  // Wait until scrolling has been quiet for a moment before checking
  window.addEventListener("scroll", function () {
    if (!current) return;
    clearTimeout(idleTimer);
    idleTimer = setTimeout(checkLanding, 160);
  }, { passive: true });
  ["wheel", "touchmove"].forEach(function (type) {
    window.addEventListener(type, stop, { passive: true });
  });

  // Arriving from another page with a link like /#quote: go to that section once the page
  // (and the loading screen, if it's showing) is ready
  const goToHash = function () {
    const target = location.hash.length > 1 && document.getElementById(location.hash.slice(1));
    if (target && !userMoved) window.scrollTo({ top: topOf(target), behavior: "instant" });
    // Clean the address again, so a link copied from here opens at the top
    if (location.hash) history.replaceState(null, "", location.pathname + location.search);
  };
  window.addEventListener("load", function () {
    if (root.classList.contains("is-loading")) document.addEventListener("cti:intro-done", goToHash, { once: true });
    else setTimeout(goToHash, 50);
  });

  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    const id = link.getAttribute("href");
    if (id.length < 2) return;
    link.addEventListener("click", function (event) {
      const target = document.getElementById(id.slice(1));
      if (!target) return;
      event.preventDefault();
      stop();
      // Don't add #section to the address, so links people copy and share open at the top
      current = target;
      window.scrollTo({ top: topOf(target), behavior: "smooth" });
      // In case the page was already in the right spot and no scrolling happens
      idleTimer = setTimeout(checkLanding, 300);
    });
  });
});

// ---------- Top slideshow ----------
// Fades to the next photo every 2 seconds and loops back to the first.
// Pauses while the tab isn't visible, and stays still for "Reduce Motion".
safely("slideshow", function () {
  const slides = Array.from(document.querySelectorAll(".hero-slides .hero-photo"));
  if (slides.length < 2) return;
  const calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const DELAY = 2000;
  let index = 0;
  let timer = null;

  const show = function (next) {
    index = (next + slides.length) % slides.length;
    slides.forEach(function (s, i) { s.classList.toggle("is-active", i === index); });
  };
  const start = function () {
    clearInterval(timer);
    if (!calm) timer = setInterval(function () { show(index + 1); }, DELAY);
  };

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) clearInterval(timer); else start();
  });
  // Wait for the loading screen before the first change
  setTimeout(start, root.classList.contains("is-loading") ? 2500 : 0);
});

// ---------- Footer year ----------
safely("footer year", function () {
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
});

// ---------- Quote form ----------
// Sends the request straight to the business Gmail through Web3Forms (free).
safely("quote form", function () {
  const form = document.getElementById("quote-form");
  if (!form) return;
  const statusText = document.getElementById("form-status");
  const success = document.getElementById("form-success");
  const button = form.querySelector(".quote-submit");
  const buttonText = button.querySelector(".label-text");
  const sendAnother = document.getElementById("send-another");
  const ENDPOINT = "https://api.web3forms.com/submit";
  let sending = false;

  form.noValidate = true; // we show our own, clearer messages

  const showError = function (html) {
    statusText.className = "form-status is-error";
    statusText.innerHTML = html;
  };
  const clearErrors = function () {
    statusText.className = "form-status";
    statusText.textContent = "";
    form.querySelectorAll(".is-invalid").forEach(function (el) {
      el.classList.remove("is-invalid");
      el.removeAttribute("aria-invalid");
    });
    form.querySelectorAll(".field-error").forEach(function (el) { el.remove(); });
  };
  const flag = function (el, message) {
    el.classList.add("is-invalid");
    el.setAttribute("aria-invalid", "true");
    // Show the message right under the field that needs fixing
    const note = document.createElement("p");
    note.className = "field-error";
    note.setAttribute("role", "alert");
    note.textContent = message;
    (el.matches(".chips") ? el : el.closest(".field") || el.parentElement).append(note);
    el.scrollIntoView({ behavior: "smooth", block: "center" });
    const focusable = el.matches("input, textarea") ? el : el.querySelector("input");
    if (focusable) setTimeout(function () { focusable.focus({ preventScroll: true }); }, 350);
  };

  // Remove the red outline as soon as the visitor fixes a field
  form.addEventListener("input", function (event) {
    const field = event.target.closest(".is-invalid") || (event.target.name === "project" && form.querySelector(".chips"));
    if (field) {
      field.classList.remove("is-invalid");
      field.removeAttribute("aria-invalid");
      const box = field.matches(".chips") ? field : field.closest(".field") || field.parentElement;
      const note = box.querySelector(".field-error");
      if (note) note.remove();
    }
  });

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    if (sending) return;
    clearErrors();

    const data = Object.fromEntries(new FormData(form));
    Object.keys(data).forEach(function (key) { data[key] = String(data[key]).trim(); });

    // Check the answers before sending
    if (!data.project) return flag(form.querySelector(".chips"), "Please choose what you're planning.");
    if (!data.name) return flag(form.elements.name, "Please enter your name.");
    if (data.phone.replace(/\D/g, "").length < 10) return flag(form.elements.phone, "Please enter a phone number with area code.");
    if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) return flag(form.elements.email, "That email doesn't look right. Check it, or leave it empty.");
    if (data.botcheck) return; // a bot ticked the hidden trap, so quietly ignore it
    delete data.botcheck;

    data.subject = "New quote request: " + data.project + " (" + data.name + ")";
    if (data.email) data.replyto = data.email; // so "Reply" in Gmail answers the customer

    sending = true;
    button.disabled = true;
    buttonText.textContent = "Sending…";

    // Give up after 15 seconds instead of spinning forever on a bad connection
    const controller = "AbortController" in window ? new AbortController() : null;
    const timeout = controller ? setTimeout(function () { controller.abort(); }, 15000) : null;

    try {
      const response = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data),
        signal: controller ? controller.signal : undefined,
      });
      // Only count it as sent when Web3Forms says so
      const result = await response.json().catch(function () { return {}; });
      if (!response.ok || String(result.success) !== "true") throw new Error(result.message || "Request failed");

      form.reset();
      form.hidden = true;
      success.hidden = false;
      success.scrollIntoView({ behavior: "smooth", block: "center" });
    } catch (error) {
      showError('Sorry, your request didn\'t go through. Please try again, or call us at <a href="tel:+16129917000">612-991-7000</a>.');
    } finally {
      clearTimeout(timeout);
      sending = false;
      button.disabled = false;
      buttonText.textContent = "Get My Free Quote";
    }
  });

  if (sendAnother) {
    sendAnother.addEventListener("click", function () {
      clearErrors();
      success.hidden = true;
      form.hidden = false;
    });
  }
});
