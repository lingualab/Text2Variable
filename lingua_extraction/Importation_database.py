import json
import pandas as pd


def read_json_file(file_name):
    """
    Lit un fichier JSON et renvoie son contenu sous forme d'un dictionnaire Python.

    Args:
        file_name (str): Le nom du fichier JSON à lire.

    Returns:
        dict ou None: Le contenu du fichier JSON sous forme de dictionnaire, ou None en cas d'erreur.
        
    Raises:
        FileNotFoundError: Si le fichier spécifié n'existe pas.
        Exception: Si une autre erreur se produit lors de la lecture du fichier.

    """
    try:
        # Tente d'ouvrir le fichier en lecture avec l'encodage UTF-8
        with open(file_name, 'r', encoding='utf-8') as file:
            # Charge le contenu JSON du fichier dans un dictionnaire Python
            content = json.load(file)
        return content
    except FileNotFoundError:
        # Gère le cas où le fichier n'existe pas
        print(f"Le fichier {file_name} n'a pas été trouvé.")
        return None
    except Exception as e:
        # Gère d'autres exceptions (par exemple, un format JSON invalide)
        print(f"Une erreur s'est produite lors de la lecture du fichier {file_name} : {str(e)}")
        return None




def lire_base_de_donnees(chemin_fichier, type_de_donnees):
    if type_de_donnees == 'frequence':
        return pd.read_excel(chemin_fichier)
    elif type_de_donnees == 'familiarite':
        return pd.read_excel(chemin_fichier, index_col='Words')
    elif type_de_donnees == 'imageabilite':
        return pd.read_excel(chemin_fichier, index_col='Words')
    elif type_de_donnees == 'concreteness':
        return pd.read_excel(chemin_fichier, index_col='Word')
    elif type_de_donnees == 'valence':
        return pd.read_excel(chemin_fichier, index_col='Word')
        
    else:
        raise ValueError("Type de données non reconnu")

