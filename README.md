# Inventaire du mobilier

Site statique MkDocs alimenté par le classeur `inventaire_mobilier.xlsx` et publié sur GitHub Pages : https://nicocoquet.github.io/inventaire-mobilier/

## Contenu du projet

- `inventaire_mobilier.xlsx` : source des fiches et des légendes ;
- `photos/` : fichiers photographiques ;
- `scripts/generate_catalog.py` : génération automatique des pages ;
- `docs/statistiques.md` : tableau de bord généré automatiquement depuis le classeur ;
- `docs/` : pages et styles du site ;
- `.github/workflows/deploy.yml` : publication automatique ;
- `mkdocs.yml` : configuration de MkDocs.

## Apparence et langues

Le site propose un thème clair et un thème sombre, sélectionnés automatiquement selon les préférences du système et modifiables depuis l’en-tête.

La structure multilingue repose sur `mkdocs-static-i18n` :

- le français (`.fr.md`) est la langue de référence, publiée à la racine du site ;
- l’anglais (`.en.md`) est publié sous `/en/` ;
- l’italien (`.it.md`) est publié sous `/it/` ;
- tant qu’une traduction n’existe pas, la fiche française sert de repli.

Pour traduire une page, dupliquez par exemple `docs/catalogue/MOB-001.fr.md` sous les noms `MOB-001.en.md` et `MOB-001.it.md`, puis traduisez leur contenu. Les chemins renseignés dans `mkdocs.yml` restent sans suffixe de langue.

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

Les instructions de saisie sont également présentes dans la troisième feuille du classeur. Elles sont volontairement conservées ici plutôt que dans la navigation du site public.

### Ajouter un meuble

1. Dans la feuille **Mobilier**, ajoutez une ligne au tableau.
2. Attribuez un identifiant unique et séquentiel (`MOB-002`, `MOB-003`, etc.).
3. Complétez les champs connus sans renommer les feuilles ni les colonnes.
4. Inscrivez **Oui** dans la colonne **Publié** lorsque la fiche peut apparaître en ligne.

Les champs inconnus peuvent rester vides.

### Ajouter plusieurs photographies

1. Renommez les images avec l’identifiant de l’objet : `MOB-002-01.jpeg`, `MOB-002-02.jpeg`, etc.
2. Placez-les dans le dossier `photos/`.
3. Dans la feuille **Photos**, ajoutez une ligne par fichier.
4. Répétez le même identifiant pour toutes les vues du même objet.
5. Attribuez un ordre et choisissez une seule image principale.

Pour masquer temporairement une fiche sans la supprimer du classeur, passez sa valeur **Publié** de **Oui** à **Non**.

## Tester localement, si nécessaire

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_catalog.py
mkdocs serve
```
