# Inventaire du mobilier

Site statique MkDocs alimenté par le classeur `inventaire_mobilier.xlsx` et publié sur GitHub Pages.

## Contenu du projet

- `inventaire_mobilier.xlsx` : source des fiches et des légendes ;
- `photos/` : fichiers photographiques ;
- `scripts/generate_catalog.py` : génération automatique des pages ;
- `docs/` : pages et styles du site ;
- `.github/workflows/deploy.yml` : publication automatique ;
- `mkdocs.yml` : configuration de MkDocs.

## Créer le dépôt GitHub

1. Sur GitHub, cliquez sur **New repository**.
2. Nommez-le par exemple `inventaire-mobilier`.
3. Choisissez **Public** si le site doit être visible de tous.
4. Ne créez pas de README, de `.gitignore` ou de licence : ils sont déjà fournis ici.
5. Importez tout le contenu de ce dossier dans la branche `main`.

## Première publication

1. Ouvrez l’onglet **Actions** du dépôt et laissez le workflow « Publier le catalogue » s’exécuter.
2. Dans **Settings → Pages**, vérifiez que la source est **Deploy from a branch**.
3. Choisissez la branche `gh-pages` et le dossier `/ (root)`, puis enregistrez.
4. Le site sera disponible à l’adresse `https://VOTRE-COMPTE.github.io/inventaire-mobilier/`.

## Mise à jour courante

1. Modifiez `inventaire_mobilier.xlsx` sans changer son nom.
2. Ajoutez les nouveaux fichiers dans `photos/`.
3. Remplacez le classeur et validez les modifications dans la branche `main`.
4. GitHub reconstruit automatiquement le catalogue.

Les instructions de saisie sont également présentes dans la troisième feuille du classeur et dans la page « Mode d’emploi » du site.

## Tester localement, si nécessaire

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_catalog.py
mkdocs serve
```

