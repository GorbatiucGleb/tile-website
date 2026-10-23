// Keep the footer year current
document.getElementById("year").textContent = new Date().getFullYear();

// Quote form: sends the request straight to the business Gmail through FormSubmit (free).
// The very first request triggers an "Activate" email that has to be clicked once.
const form = document.getElementById("quote-form");
const statusText = document.getElementById("form-status");

form.addEventListener("submit", async function (event) {
  event.preventDefault();
  const button = form.querySelector("button");
  const data = Object.fromEntries(new FormData(form));

  data._subject = "New quote request: " + data.project + " (" + data.name + ")";
  data._template = "table";
  data._captcha = "false";
  if (data.email) data._replyto = data.email;

  button.disabled = true;
  button.textContent = "Sending…";
  statusText.className = "form-status";
  statusText.textContent = "";

  try {
    const response = await fetch("https://formsubmit.co/ajax/agcustomtileinteriors@gmail.com", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Request failed");

    form.reset();
    statusText.classList.add("is-success");
    statusText.textContent = "Thank you! Your request was sent. We'll get back to you soon.";
  } catch (error) {
    statusText.classList.add("is-error");
    statusText.innerHTML = 'Sorry, something went wrong. Please call us at <a href="tel:+16129917000">612-991-7000</a>.';
  } finally {
    button.disabled = false;
    button.textContent = "Send Request";
  }
});
