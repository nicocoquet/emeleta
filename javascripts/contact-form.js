document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;

  // Adresse provisoire centralisée ici : elle pourra être remplacée par
  // contact@emeleta.it sans modifier les trois pages traduites.
  const recipient = "nc1206@gmail.com";
  const locale = document.documentElement.lang?.slice(0, 2) || "fr";
  const labels = {
    fr: { defaultSubject: "Message depuis Trinketa", name: "Nom", email: "Adresse" },
    en: { defaultSubject: "Message from Trinketa", name: "Name", email: "Email address" },
    it: { defaultSubject: "Messaggio da Trinketa", name: "Nome", email: "Indirizzo e-mail" },
  }[locale] || { defaultSubject: "Message depuis Trinketa", name: "Nom", email: "Adresse" };

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const data = new FormData(form);
    const subject = encodeURIComponent(data.get("subject") || labels.defaultSubject);
    const body = encodeURIComponent(
      `${labels.name} : ${data.get("name")}\n${labels.email} : ${data.get("email")}\n\n${data.get("message")}`
    );
    window.location.href = `mailto:${recipient}?subject=${subject}&body=${body}`;
  });
});
