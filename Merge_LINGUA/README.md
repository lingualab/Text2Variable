# Bibliothèque Python 


## Fonctionnalités Principales

Pour exécuter le code, vous pouvez utiliser la commande suivante :

```bash
python main.py mon_fichier_input.json
```

Lorsque vous lancez le code de cette manière, il lira le fichier JSON d'entrée spécifié (mon_fichier_input.json dans cet exemple) et effectuera le traitement des données. Par défaut, le fichier de sortie sera enregistré dans un dossier appelé "Results".

Cependant, si vous souhaitez spécifier un nom de fichier de sortie personnalisé, vous pouvez utiliser l'option -o (ou --output_name) comme ceci :

```bash
python main.py mon_fichier_input.json -o mon_fichier_output
```

Dans cet exemple, le code enregistrera le fichier de sortie avec le nom mon_fichier_output.json au lieu de l'utiliser le nom par défaut.

Si vous préférez enregistrer le fichier de sortie dans un dossier spécifique de votre choix, vous pouvez utiliser l'option -d (ou --output_dir) pour spécifier le dossier de sortie. Par exemple :

```bash
python main.py mon_fichier_input.json -d DossierPersonnel
```

Dans cette variante, le fichier de sortie sera enregistré dans le dossier DossierPersonnel. Vous avez donc la flexibilité de choisir où vous souhaitez stocker le fichier de sortie en utilisant l'option -d.

Cela vous permet de personnaliser le nom du fichier de sortie et le dossier de sortie en fonction de vos besoins lors de l'exécution du code.

## Installation

Pour installer cette bibliothèque, vous pouvez utiliser `pip`:

```bash
pip install lingua_merge
```

## Contribution
Nous sommes ouverts aux contributions de la communauté. Si vous souhaitez contribuer à cette bibliothèque, veuillez consulter notre guide de contribution ici.

## Licence
Cette bibliothèque est distribuée sous la licence MIT. Veuillez consulter le fichier LICENCE pour plus d'informations.

## Contact
Pour toute question ou commentaire, n'hésitez pas à nous contacter à l'adresse : pierre-briac.metayer--mariotti@umontreal.ca.

