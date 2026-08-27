# Trinketa

Site statique MkDocs d'inventaire du mobilier et des livres anciens, alimenté par les classeurs `inventaire_mobilier.xlsx` et `inventaire_bibliotheque.xlsx`, publié sur GitHub Pages : https://nicocoquet.github.io/trinketa/

## Comment fonctionne la génération

Les deux classeurs et le dossier `photos/` sont les sources de référence. Les
pages de catalogue ne doivent pas être corrigées à la main : elles sont recréées
à chaque déploiement dans cet ordre :

1. `scripts/generate_mobilier.py` produit le catalogue du mobilier et la page
   Statistiques commune ;
2. `scripts/generate_bibliotheque.py` produit le catalogue des livres et le
   fichier `docs/assets/data/bibliotheque-statistiques.json` ;
3. MkDocs transforme le dossier `docs/` en site statique et le publie.

Le fichier JSON des statistiques est une sortie technique générée. Le
JavaScript le lit dans le navigateur pour construire les indicateurs, les
graphiques, les filtres et la carte. Il ne faut pas le modifier manuellement.

Pour vérifier localement l'ensemble du processus :

```bash
python -m pip install -r requirements.txt
python scripts/generate_mobilier.py
python scripts/generate_bibliotheque.py
mkdocs build --strict
```

## Inventaire du mobilier

### Mise à jour courante

1. Modifier `inventaire_mobilier.xlsx` sans changer son nom ;
2. Ajouter les nouveaux fichiers dans `photos/` ;
3. Remplacer le classeur et valider les modifications dans la branche `main`.

### Ajouter un objet dans l'inventaire

1. Ajouter une ligne au tableau dans la feuille **Mobilier** ;
2. Attribuer un identifiant unique et séquentiel (`MOB-002`, `MOB-003`, etc.) ;
3. Compléter les champs connus sans renommer les feuilles ni les colonnes ;
4. Inscrire **Oui** dans la colonne **Publié** lorsque la fiche peut apparaître en ligne.

Les champs inconnus peuvent rester vides.

### Ajouter des photographies

1. Renommer les images avec l’identifiant de l’objet : `MOB-002-01.jpeg`, `MOB-002-02.jpeg`, etc. ;
2. Les placer dans le dossier `photos/` ;
3. Ajouter une ligne par fichier dans la feuille **Photos** ;
4. Répéter le même identifiant pour toutes les vues du même objet ;
5. Attribuer un ordre et choisir une seule image principale.

Pour masquer temporairement une fiche sans la supprimer du classeur, passez sa valeur **Publié** de **Oui** à **Non**.

## Bibliothèque

### Mise à jour courante

1. Modifier `inventaire_bibliotheque.xlsx` sans changer son nom.
2. Ajouter les nouveaux fichiers dans `photos/bibliotheque`.
3. Remplacer le classeur et valider les modifications dans la branche `main`.

### Ajouter un objet dans l'inventaire

#### Avec ISBN
#### Sans ISBN

Les champs inconnus peuvent rester vides.

### Ajouter des photographies

Pour masquer temporairement une fiche sans la supprimer du classeur, passez sa valeur **Publié** de **Oui** à **Non**.

## Statistiques

La page **Statistiques** réunit dans une même vue :

- les estimations et répartitions du mobilier ;
- les indicateurs, graphiques et la carte des lieux d’édition de la bibliothèque.

Elle est régénérée automatiquement à partir des deux classeurs lors de chaque déploiement. Le script du mobilier construit la page unifiée, puis le script de la bibliothèque produit le jeu de données interactif consommé par cette page.
