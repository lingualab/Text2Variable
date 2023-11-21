# Fonction de suppression des stop words
def supprimer_stop_words(tokens, modele):
    """
    Supprime les stop words des tokens.

    Args:
    tokens (List[str]): Liste des tokens.
    modele (str): Le modèle spaCy à utiliser.

    Returns:
    List[str]: Tokens sans stop words.
    """
    nlp = modele
    return [token for token in tokens if not nlp.vocab[token].is_stop]