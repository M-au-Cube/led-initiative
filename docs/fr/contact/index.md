# Contact

<div class="led-contact-grid" markdown="1">

<div class="led-contact-card" markdown="1">

## Nous écrire

**Email :** [{{ config.extra.contact_email }}](mailto:{{ config.extra.contact_email }})

**Site :** [led-initiative.fr](https://led-initiative.fr)

Pour toute question sur le programme, les adhésions ou la presse, écrivez-nous directement par email.

</div>

<div class="led-contact-card" markdown="1">

## Formulaire de contact

<form class="led-contact-form" action="https://formspree.io/f/{{ config.extra.formspree_form_id }}" method="POST">
  <input type="hidden" name="_subject" value="Contact LED — led-initiative.fr">
  <input type="hidden" name="_language" value="fr">
  <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
  <label for="name">Nom</label>
  <input type="text" id="name" name="name" required placeholder="Votre nom">
  <label for="email">Email</label>
  <input type="email" id="email" name="email" required placeholder="votre@email.fr">
  <label for="subject">Sujet</label>
  <select id="subject" name="subject">
    <option value="programme">Question sur le programme</option>
    <option value="adhesion">Adhésion / engagement</option>
    <option value="presse">Presse</option>
    <option value="autre">Autre</option>
  </select>
  <label for="message">Message</label>
  <textarea id="message" name="message" rows="5" required placeholder="Votre message…"></textarea>
  <button type="submit">Envoyer</button>
</form>

!!! tip "Configuration Formspree"
    L'identifiant du formulaire est défini dans `mkdocs.yml` (`extra.formspree_form_id`). Créez un compte gratuit sur [Formspree](https://formspree.io/) et un formulaire ciblant **{{ config.extra.contact_email }}**.

</div>

</div>

---

[Retour à l'accueil](/)
