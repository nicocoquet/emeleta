<header class="contact-heading">
  <p class="eyebrow">Scrivici</p>
  <h1>Contatto</h1>
  <p>Può scriverci in italiano, francese, inglese o spagnolo.</p>
</header>

<form class="contact-form" data-contact-form>
  <div class="contact-field">
    <label for="contact-name">Nome</label>
    <input id="contact-name" name="name" type="text" autocomplete="name" required>
  </div>
  <div class="contact-field">
    <label for="contact-email">Indirizzo e-mail</label>
    <input id="contact-email" name="email" type="email" autocomplete="email" required>
  </div>
  <div class="contact-field contact-field-wide">
    <label for="contact-subject">Oggetto</label>
    <input id="contact-subject" name="subject" type="text" required>
  </div>
  <div class="contact-field contact-field-wide">
    <label for="contact-message">Messaggio</label>
    <textarea id="contact-message" name="message" rows="8" required></textarea>
  </div>
  <div class="contact-actions contact-field-wide">
    <button type="submit">Invia<span>→</span></button>
    <p class="contact-status">L’invio aprirà l’applicazione di posta elettronica.</p>
  </div>
</form>
