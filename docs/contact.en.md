<header class="contact-heading">
  <p class="eyebrow">Write to us</p>
  <h1>Contact</h1>
  <p>You can write to us in Italian, French, English or Spanish.</p>
</header>

<form class="contact-form" data-contact-form data-recipient="">
  <div class="contact-field">
    <label for="contact-name">Name</label>
    <input id="contact-name" name="name" type="text" autocomplete="name" required>
  </div>
  <div class="contact-field">
    <label for="contact-email">Email address</label>
    <input id="contact-email" name="email" type="email" autocomplete="email" required>
  </div>
  <div class="contact-field contact-field-wide">
    <label for="contact-subject">Subject</label>
    <input id="contact-subject" name="subject" type="text" required>
  </div>
  <div class="contact-field contact-field-wide">
    <label for="contact-message">Message</label>
    <textarea id="contact-message" name="message" rows="8" required></textarea>
  </div>
  <div class="contact-actions contact-field-wide">
    <button type="submit">Send<span>→</span></button>
    <p class="contact-status" data-contact-status aria-live="polite">The destination address will be configured in the next step.</p>
  </div>
</form>
