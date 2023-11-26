import json
import os

def save_json_file(output_path, data):
    """
    Enregistre un dictionnaire Python au format JSON dans un fichier.

    Args:
        output_path (str): Le chemin complet du fichier JSON de sortie.
        data (dict): Les données à enregistrer.

    Returns:
        bool: True si l'enregistrement a réussi, False sinon.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'enregistrement du fichier {output_path}: {str(e)}")
        return False
