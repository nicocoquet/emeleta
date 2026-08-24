<header class="contact-heading">
  <p class="eyebrow">Écrire à la collection</p>
  <h1>Contacts</h1>
  <p>Une question, une précision ou une piste de recherche concernant un objet de l’inventaire&nbsp;? Laissez-nous un message.</p>
</header>

<form class="contact-form" data-contact-form data-recipient="">
  <div class="contact-field">
    <label for="contact-name">Nom</label>
    <input id="contact-name" name="name" type="text" autocomplete="name" required>
  </div>
  <div class="contact-field">
    <label for="contact-email">Adresse électronique</label>
    <input id="contact-email" name="email" type="email" autocomplete="email" required>
  </div>
  <div class="contact-field contact-field-wide">
    <label for="contact-subject">Objet</label>
    <input id="contact-subject" name="subject" type="text" required>
  </div>
  <div class="contact-field contact-field-wide">
    <label for="contact-message">Message</label>
    <textarea id="contact-message" name="message" rows="8" required></textarea>
  </div>
  <div class="contact-actions contact-field-wide">
    <button type="submit">Envoyer le message <span>→</span></button>
    <p class="contact-status" data-contact-status aria-live="polite">L’adresse de destination sera configurée lors de la prochaine étape.</p>
  </div>
</form>
