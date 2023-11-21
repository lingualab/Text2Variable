# Fonction de lemmatisation
def lemmatiser_texte(texte, modele):
    """
    Lemmatise le texte.

    Args:
    texte (str): Le texte à lemmatiser.
    modele (str): Le modèle spaCy à utiliser.

    Returns:
    List[str]: Liste des lemmes.
    """
    nlp = modele
    doc = nlp(texte)
    return [token.lemma_ for token in doc if not token.is_stop]