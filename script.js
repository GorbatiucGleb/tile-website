// Keep the footer year current
document.getElementById("year").textContent = new Date().getFullYear();

// Quote form: opens the visitor's email app with the details filled in.
// TODO: swap for a form service (like Formspree) so requests send straight from the page.
document.getElementById("quote-form").addEventListener("submit", function (event) {
  event.preventDefault();
  const form = new FormData(event.target);

  const subject = "Quote request: " + form.get("project");
  const body =
    "Name: " + form.get("name") + "\n" +
    "Phone: " + form.get("phone") + "\n" +
    "City: " + form.get("city") + "\n" +
    "Project: " + form.get("project") + "\n\n" +
    form.get("details");

  window.location.href =
    "mailto:agcustomtileinteriors@gmail.com" +
    "?subject=" + encodeURIComponent(subject) +
    "&body=" + encodeURIComponent(body);
});
