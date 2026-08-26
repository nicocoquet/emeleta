#Emeleta

Site statique MkDocs d'inventaire de mobilier et livres anciens, alimenté par les classeurs `inventaire_mobilier.xlsx` et `inventaire_bibliotheque.xlsx`, et publié sur GitHub Pages : [Emeleta](https://nicocoquet.github.io/emeleta/)

![Emeleta](docs/assets/images/preview.jpeg)

## Inventaire du mobilier

### Mise à jour courante

1. Modifiez `inventaire_mobilier.xlsx` sans changer son nom.
2. Ajoutez les nouveaux fichiers dans `photos/`.
3. Remplacez le classeur et validez les modifications dans la branche `main`.
4. GitHub reconstruit automatiquement le catalogue.

### Ajouter un objet dans l'inventaire

1. Dans la feuille **Mobilier**, ajoutez une ligne au tableau.
2. Attribuez un identifiant unique et séquentiel (`MOB-002`, `MOB-003`, etc.).
3. Complétez les champs connus sans renommer les feuilles ni les colonnes.
4. Inscrivez **Oui** dans la colonne **Publié** lorsque la fiche peut apparaître en ligne.

Les champs inconnus peuvent rester vides.

### Ajouter des photographies

1. Renommez les images avec l’identifiant de l’objet : `MOB-002-01.jpeg`, `MOB-002-02.jpeg`, etc.
2. Placez-les dans le dossier `photos/`.
3. Dans la feuille **Photos**, ajoutez une ligne par fichier.
4. Répétez le même identifiant pour toutes les vues du même objet.
5. Attribuez un ordre et choisissez une seule image principale.

Pour masquer temporairement une fiche sans la supprimer du classeur, passez sa valeur **Publié** de **Oui** à **Non**.

## Bibliothèque

### Mise à jour courante

1. Modifiez `inventaire_bibliotheque.xlsx` sans changer son nom.
2. Ajoutez les nouveaux fichiers dans `photos/bibliotheque`.
3. Remplacez le classeur et validez les modifications dans la branche `main`.
4. GitHub reconstruit automatiquement le catalogue.

### Ajouter un objet dans l'inventaire

#### Avec ISBN
#### Sans ISBN

Les champs inconnus peuvent rester vides.

### Ajouter des photographies

Pour masquer temporairement une fiche sans la supprimer du classeur, passez sa valeur **Publié** de **Oui** à **Non**.
