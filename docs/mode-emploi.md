# Mettre à jour le catalogue

Le fichier `inventaire_mobilier.xlsx` est la source du site. Les pages du catalogue sont recréées automatiquement à partir de son contenu.

## Ajouter un meuble

1. Ouvrez `inventaire_mobilier.xlsx`.
2. Dans la feuille **Mobilier**, ajoutez une ligne au tableau.
3. Donnez à l’objet un identifiant unique : `MOB-002`, puis `MOB-003`, etc.
4. Complétez les champs disponibles.
5. Inscrivez **Oui** dans la colonne **Publié** lorsque la fiche peut apparaître en ligne.

Les champs inconnus peuvent rester vides. Il ne faut ni renommer les feuilles, ni modifier les intitulés des colonnes.

## Ajouter plusieurs photographies

1. Renommez les images avec l’identifiant du meuble : `MOB-002-01.jpeg`, `MOB-002-02.jpeg`, etc.
2. Placez-les dans le dossier `photos` du dépôt.
3. Dans la feuille **Photos**, ajoutez une ligne par fichier.
4. Répétez le même identifiant d’objet pour toutes les vues concernées.
5. Attribuez un ordre et choisissez une seule image principale.

## Publier

Sur GitHub, remplacez le classeur par sa nouvelle version et ajoutez les nouvelles photographies. Après validation des modifications, l’automatisation reconstruit et republie le site. La publication prend généralement quelques minutes.

## Masquer temporairement une fiche

Passez la valeur **Publié** de **Oui** à **Non**. La ligne demeure dans Excel, mais la fiche disparaît du site lors de la publication suivante.

