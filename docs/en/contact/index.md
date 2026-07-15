# Contact

<div class="led-contact-grid" markdown="1">

<div class="led-contact-card" markdown="1">

## Write to us

**Email:** [{{ config.extra.contact_email }}](mailto:{{ config.extra.contact_email }})

**Website:** [led-initiative.fr](https://led-initiative.fr)

For any questions about the program, membership or press inquiries, write to us directly by email.

</div>

<div class="led-contact-card" markdown="1">

## Contact form

<form class="led-contact-form" action="https://formspree.io/f/{{ config.extra.formspree_form_id }}" method="POST">
  <input type="hidden" name="_subject" value="LED contact — led-initiative.fr">
  <input type="hidden" name="_language" value="en">
  <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
  <label for="name">Name</label>
  <input type="text" id="name" name="name" required placeholder="Your name">
  <label for="email">Email</label>
  <input type="email" id="email" name="email" required placeholder="your@email.com">
  <label for="subject">Subject</label>
  <select id="subject" name="subject">
    <option value="program">Question about the program</option>
    <option value="membership">Membership / engagement</option>
    <option value="press">Press</option>
    <option value="other">Other</option>
  </select>
  <label for="message">Message</label>
  <textarea id="message" name="message" rows="5" required placeholder="Your message…"></textarea>
  <button type="submit">Send</button>
</form>

!!! tip "Formspree setup"
    The form ID is set in `mkdocs.yml` (`extra.formspree_form_id`). Create a free account on [Formspree](https://formspree.io/) and a form targeting **{{ config.extra.contact_email }}**.

</div>

</div>

<div class="led-contact-logo">
  <img src="/assets/images/logo-led.png" alt="LED — Liberty Environment Democracy">
</div>

---

[Back to home](/en/)
