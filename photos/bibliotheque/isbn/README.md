# File d’ingestion ISBN

Ce répertoire est le point d’entrée des photographies de codes-barres pour la bibliothèque Emeleta.

- `a_traiter/` : déposer ici les nouvelles photographies de codes-barres ISBN.
- `a_verifier/` : cas qui nécessitent une intervention humaine (ISBN illisible, édition ambiguë, sources contradictoires non résolues, etc.).
- `traite/` : photographies ayant produit une notice validée et publiée.

## Règle d’usage

1. Déposer une ou plusieurs images dans `a_traiter/` puis pousser sur GitHub.
2. Demander dans ChatGPT : « traite la file ISBN ».
3. Le traitement attribue automatiquement le prochain identifiant `BIB-xxx` disponible, enrichit la notice, alimente le pipeline, publie le site et contrôle la page générée.
4. Une image validée est archivée sous la forme `BIB-xxx_isbn_<ISBN13>.<extension>` dans `traite/`.
5. Une image qui ne peut pas être traitée de façon sûre est déplacée dans `a_verifier/` et consignée dans le journal technique.

Le tableur `inventaire_bibliotheque.xlsx` reste la base éditoriale. Le fichier `data/bibliotheque/imports/journal.csv` est uniquement le journal d’ingestion et de traçabilité.
