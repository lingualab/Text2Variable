class TraitementDuTexte:
    def __init__(self, texte, nlp):
        # Initialise la classe avec un texte et un modèle de traitement du langage naturel (NLP).
        self.texte = texte
        self.nlp = nlp

    def traiter(self):
        """
        Traite le texte en le tokenisant, en le nettoyant et en le lemmatisant.

        Applique le traitement du texte au texte fourni.
        Les étapes incluent la tokenisation, le nettoyage (en supprimant la ponctuation
        et en mettant en minuscules), et la lemmatisation.
        
        Returns:
            list: Liste de tokens lemmatisés et nettoyés.
        """
        # Appelle les méthodes pour effectuer le traitement.
        tokens = self.tokeniser_et_nettoyer()
        lemmes = self.lemmatiser(tokens)

        # Affiche un message de confirmation.
        print("Le traitement du texte a été effectué avec succès.")
        print("Le texte a été tokenisé, nettoyé et lemmatisé.")

        return lemmes

    def tokeniser_et_nettoyer(self):
        """
        Tokenise le texte et supprime la ponctuation.

        Cette méthode tokenise le texte en mots et supprime la ponctuation,
        en mettant également tout en minuscule.
        
        Returns:
            list: Liste de tokens nettoyés.
        """
        tokens = [token.text.lower() for token in self.nlp(self.texte) if not token.is_punct]
        return tokens

    def lemmatiser(self, tokens):
        """
        Effectue la lemmatisation des tokens.

        Pour chaque token nettoyé, cette méthode trouve le lemme correspondant.
        
        Args:
            tokens (list): Liste de tokens nettoyés.
            
        Returns:
            list: Liste des lemmes pour chaque token.
        """
        lemmes = [token.lemma_ for token in self.nlp(' '.join(tokens))]
        return lemmes
