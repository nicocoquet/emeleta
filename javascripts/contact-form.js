document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const status = form.querySelector("[data-contact-status]");
    const recipient = form.dataset.recipient?.trim();

    if (!recipient) {
      status.textContent = "Le formulaire est prêt : il reste à renseigner l’adresse de destination.";
      status.classList.add("contact-status-alert");
      return;
    }

    const data = new FormData(form);
    const subject = encodeURIComponent(data.get("subject") || "Message depuis l’inventaire");
    const body = encodeURIComponent(
      `Nom : ${data.get("name")}\nAdresse : ${data.get("email")}\n\n${data.get("message")}`
    );
    window.location.href = `mailto:${recipient}?subject=${subject}&body=${body}`;
  });
});
