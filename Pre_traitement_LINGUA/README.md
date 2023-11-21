# Lingua Pre-Processing

Lingua Pre-Processing est une bibliothèque Python conçue pour préparer le texte pour les analyses de traitement automatique du langage naturel (NLP). Elle offre une gamme de fonctionnalités pour nettoyer, tokeniser, supprimer les stop words et lemmatiser le texte.

## Fonctionnalités Principales : 

- Nettoyage du texte : Retire les éléments inutiles ou perturbateurs dans le texte, tels que les identifiants et les éléments de formatage.

- Tokenisation : Divise le texte en mots ou en "tokens".

- Suppression des Stop Words : Élimine les mots courants qui portent peu d'information utile.

- Lemmatisation : Réduit les mots à leur forme de base ou "lemme", en prenant en compte le contexte.

## Installation

Pour installer cette bibliothèque, utilisez pip :

```bash
pip install lingua_pre_processing
```
Il faut ensuite installer les modèles Spacy que vous souhaitez utiliser

Voici les modèles déjà enregistré :

```json
Francais: {
            "sm": "fr_core_news_sm",
            "md": "fr_core_news_md",
            "lg": "fr_core_news_lg",
            "trf": "fr_dep_news_trf",
            }

English: {
            "sm": "en_core_web_sm",
            "md": "en_core_web_md",
            "lg": "en_core_web_lg",
            "trf": "en_core_web_trf",
            }
```

## Exemple

Voici un exemple afin de traiter le texte contenu dans un fichier.
Le fichier contient l'ID, la langue et le texte.

Voici l'organisation que l'on doit avoir :

```json
{
    "ID": "BCG14703",

    "Langue": "English",

    "Texte": "Langue: English\nID: BCG14703\nTexte complet des interventions:\nI see a small uhummm kitchen with a table in the center. There is a child standing on a uhummm stool, trying to reach for cookies on the table. A woman is standing near... the sink, washing dishes, and she seems not to notice the child. The image gives me a feeling ... of chaos and disorder in the kitchen."
}
```

Ici on lance le prétraitement sur le texte avec le modèle sm.

Voici la liste des modèles disponibles : https://spacy.io/models/en

```python
python src/main.py Results/BCG14703.json sm
```

## Contribution
Nous sommes ouverts aux contributions de la communauté. Si vous souhaitez contribuer à cette bibliothèque, veuillez consulter notre guide de contribution ici.

## Licence
Cette bibliothèque est distribuée sous la licence MIT. Veuillez consulter le fichier LICENCE pour plus d'informations.

## Contact
Pour toute question ou commentaire, n'hésitez pas à nous contacter à l'adresse : pierre-briac.metayer--mariotti@umontreal.ca.

