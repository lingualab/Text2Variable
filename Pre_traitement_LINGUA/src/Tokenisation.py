# Fonction de tokenisation
def tokeniser_texte(texte, modele):
    """
    Tokenise le texte en utilisant spaCy.

    Args:
    texte (str): Le texte à tokeniser.
    modele (str): Le modèle spaCy à utiliser.

    Returns:
    List[str]: Liste des tokens.
    """
    nlp = modele
    doc = nlp(texte)
    return [token.text for token in doc]