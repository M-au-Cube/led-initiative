# LED Initiative — Site web

Site statique bilingue (FR/EN) du parti **LED** (Liberté, Environnement, Démocratie), construit avec [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) et hébergé sur **GitHub Pages** à l'adresse [led-initiative.fr](https://led-initiative.fr).

## Structure

| Page | FR | EN |
|------|----|----|
| Accueil | `/` | `/en/` |
| Programme | `/programme/` | `/en/programme/` |
| Fiches PDF | `/mesures/` | `/en/mesures/` |
| Vote | `/vote/` | `/en/vote/` |
| Manifeste | `/manifeste/` | `/en/manifeste/` |
| Contact | `/contact/` | `/en/contact/` |

## Développement local

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python scripts/generate_pdfs.py
mkdocs serve
```

Le site est accessible sur [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Contenu et PDFs

Les mesures du programme sont définies dans `data/measures.yaml` (source unique). Le script `scripts/generate_pdfs.py` génère :

- le programme général (FR + EN)
- une fiche PDF par mesure (FR + EN)
- le fichier JSON `docs/assets/data/measures.json` pour le site et le vote

## Déploiement GitHub Pages

1. Poussez le dépôt sur GitHub
2. **Settings → Pages → Source** : sélectionnez **GitHub Actions**
3. Le workflow `.github/workflows/deploy.yml` build et déploie automatiquement
4. Configurez le domaine personnalisé `led-initiative.fr` :
   - Fichier `CNAME` déjà présent
   - DNS : enregistrement `CNAME` ou `A` vers GitHub Pages

## Configuration à personnaliser

| Élément | Fichier |
|---------|---------|
| URL de pétition (manifeste) | `mkdocs.yml` → `extra.manifeste_url` |
| Formulaire de contact (Formspree) | `mkdocs.yml` → `extra.formspree_form_id` |
| Vote agrégé (Supabase) | `docs/assets/js/voting-config.js` |
| Email | `mkdocs.yml` → `extra.contact_email` |

### Configurer Formspree (formulaire de contact)

1. Créez un compte sur [formspree.io](https://formspree.io/)
2. **New form** → adresse de réception : `contact@led-initiative.fr`
3. Copiez l'identifiant du formulaire (partie après `/f/` dans l'URL, ex. `xrgwkpvn`)
4. Collez-le dans `mkdocs.yml` :

```yaml
extra:
  formspree_form_id: xrgwkpvn
```

## Vote sur les mesures

Par défaut, les votes sont enregistrés **localement** dans le navigateur (mode démonstration). Pour une agrégation nationale, configurez [Supabase](https://supabase.com) dans `voting-config.js` (mode `supabase`).

## Licence

© 2026 LED Initiative
