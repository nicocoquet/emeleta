# Inventaire du mobilier

Site statique MkDocs alimenté par un classeur `inventaire_mobilier.xlsx` et publié sur GitHub Pages : https://nicocoquet.github.io/inventaire-mobilier/

## Ajouter un objet au catalogue

1. Ouvrir `inventaire_mobilier.xlsx` ;
2. Dans la feuille **Mobilier**, ajouter une ligne au tableau ;
3. Donner à l’objet un identifiant unique (sur le modèle `MOB-002`, `MOB-003`, etc.) ;
4. Compléter les champs disponibles ;
5. Noter **Oui** dans la colonne **Publié** lorsque la fiche peut apparaître en ligne.

Les champs inconnus peuvent rester vides. Il ne faut ni renommer les feuilles, ni modifier les intitulés des colonnes.

## Ajouter des photographies

1. Renommer les images avec l’identifiant du meuble (`MOB-002-01.jpeg`, `MOB-002-02.jpeg`, etc.) ;
2. Les placer dans le dossier `photos` du dépôt ;
3. Dans la feuille **Photos**, ajouter une ligne par fichier ;
4. Répéter le même identifiant d’objet pour toutes les vues concernées ;
5. Attribuer un ordre et choisir une seule image principale.

## Publication

Sur GitHub, remplacer le classeur par sa nouvelle version et ajouter les nouvelles photographies. Après validation des modifications, l’automatisation reconstruit et republie le site.

## Masquer temporairement une fiche

Passer la valeur **Publié** de **Oui** à **Non**. La ligne demeure dans le tableur Excel, mais la fiche disparaît du site lors de la publication suivante.
