import re

# Fonction de nettoyage du texte
def nettoyer_texte(texte):
    """
    Nettoie le texte en effectuant plusieurs opérations de nettoyage.

    Args:
    texte (str): Le texte à nettoyer.

    Returns:
    str: Texte nettoyé.
    """

    # Supprime le contenu entre crochets ([...])
    texte = re.sub(r"\[.*?\]", "", texte)

    # Supprime la ponctuation, en conservant les lettres, les apostrophes, les espaces, les points et les points d'interrogation
    texte = re.sub(r"[^\w\’ \.\?]", "", texte)

    # Supprime les points qui suivent un espace
    texte = re.sub(r"\s\.", "", texte)

    # Remplace deux espaces consécutifs par un seul espace
    texte = re.sub(r"\s\s+", " ", texte)

    return texte
