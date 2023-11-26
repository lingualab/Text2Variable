# Bibliothèque Python 

## Description

Ce script Python est conçu pour extraire des variables d'un texte afin de réaliser des analyses par la suite.

## Dépendances
- Python 3.x
- spaCy
- Un modèle de spaCy (sm, md, lg, ou trf)

## Installation

Avant d'exécuter ce script, assurez-vous d'avoir installé Python et spaCy. Vous pouvez installer spaCy en utilisant pip :

```bash
pip install spacy
```

### Spacy

Pour télécharger un modèle spaCy, utilisez la commande suivante :

```bash
python -m spacy download [nom_du_modèle]
```

Remplacez `[nom_du_modèle]` par `en_core_web_sm`, `en_core_web_md`, `en_core_web_lg`, ou `en_core_web_trf`, selon vos besoins.

## Utilisation

Pour utiliser le script, vous devez fournir un fichier JSON d'entrée contenant les données d'interventions. Le script accepte les arguments suivants :

- `input_name`: Nom du fichier JSON d'entrée.

- `Taille_model_spacy`: Taille du modèle spaCy (sm, md, lg, trf).

- `-o` ou `--output_name` (optionnel): Nom du fichier JSON de sortie.

- `-d` ou `--output_dir` (optionnel): Dossier de sortie.

Exemple d'utilisation :

```bash
python main.py interventions.json lg -o output.json -d /chemin/du/dossier
```

Vous pouvez tester le code avec ce input : 

```bash
python src/main.py Results/BCG14703.json sm
```

## Sortie

Le script génère un fichier JSON contenant les interventions analysées. Si aucun nom de fichier de sortie n'est spécifié, le script utilisera un nom par défaut. Le dossier de sortie peut également être spécifié ; sinon, le fichier sera enregistré dans le dossier courant.


## Fonctionnalités Principales

La bibliothèque comprend les modules suivants :

## Installation

Pour installer cette bibliothèque, vous pouvez utiliser `pip`:

```bash
pip install lingua_extraction
```

### Contribution
Nous sommes ouverts aux contributions de la communauté. Si vous souhaitez contribuer à cette bibliothèque, veuillez consulter notre guide de contribution ici.

### Licence
Cette bibliothèque est distribuée sous la licence MIT. Veuillez consulter le fichier LICENCE pour plus d'informations.

### Contact
Pour toute question ou commentaire, n'hésitez pas à nous contacter à l'adresse : pierre-briac.metayer--mariotti@umontreal.ca.

