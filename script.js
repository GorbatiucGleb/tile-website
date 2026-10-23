// Always open at the top of the page (phones otherwise jump back to where you last were),
// unless the link points at a section like #quote
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
window.addEventListener("load", function () {
  if (!location.hash) window.scrollTo(0, 0);
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
