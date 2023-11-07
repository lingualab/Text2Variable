import more_itertools

class AnalyseFragmentaire:

    def __init__(self, donnees, langue):
        # Initialise la classe avec les données fournies et la langue spécifiée.
        self.donnees = donnees
        self.langue = langue.lower()
        self.words_target = self._define_words_target()

    def _define_words_target(self):
        """Définit les paires de mots cibles en fonction de la langue."""
        words_targets = {
            'english': [('the', 'there'), ('dry', 'or'), ('out', 'outside'), ('wash', 'drying'), ('curt', 'the'), ('is', 'spill'), ('wash', 'is'), ('bow', 'Cup'), ('tap', 'taps'),
                   ('spill', 'is'), ('kit', 'the'), ('stand', 'standing'), ('go', 'reaching'), ('dish', 'The'), ('look', 'uh'), ('dry', 'or'), ('watch', 'washing'), ('sleeve', 'sleeveless'),
                   ('cook', 'cookie'), ('a', 'an'), ('day', 'daytime'), ('curt', 'the'), ('look', 'reaching'), ('sister', 'reach'), ('cab', 'the'), ('cook', 'the'), ('stand', 'climbing'), ('her','ask'),
                   ('ask', 'asking'), ('up', 'upper')],
            'francais': [('le', 'là'), ('sec', 'ou'),]  # Ceci est une fausse liste de paires de mots cibles en français
        }
        return words_targets.get(self.langue, "La langue spécifiée n'est pas disponible pour le moment.")

    def _rem_punct(self, sample):
        """Supprime les ponctuations d'un échantillon."""
        punct_and_spaces = ["?", "!", ".", "’", "'", "...", "-", " "]
        return [mot for mot in sample if mot not in punct_and_spaces]

    def supprimer_ponctuation(self):
        """
        Supprime la ponctuation de plusieurs colonnes de données.
        """
        cols = ['lemmaNouns', 'lemmaVerbs', 'lemmaAdj', 'lemmaAll', 'Texte_traité']
        for col in cols:
            # On vérifie d'abord si la clé existe dans le dictionnaire
            if col in self.donnees:
                self.donnees[col] = self._rem_punct(self.donnees[col])
        # Calcul du nombre total de mots après la suppression de la ponctuation
        if 'lemmaAll' in self.donnees:
            self.donnees['numWords'] = len(self.donnees['lemmaAll'])
        print("La suppression de la ponctuation a été effectuée avec succès.")
        return self.donnees

    def _context_fragments(self, tokens):
        """Compte les fragments en contexte en fonction de la langue."""
        if isinstance(self.words_target, str):
            print(self.words_target)
            return 0

        combs = list(more_itertools.windowed(tokens, 2))
        return sum(f in self.words_target for f in combs)

    def compter_fragments_contexte(self):
        """
        Compte les fragments en contexte pour chaque ligne de données.
        """
        if 'Texte_traité' in self.donnees:
            self.donnees['context_fragments'] = self._context_fragments(self.donnees['Texte_traité'])
        print("Le comptage des fragments en contexte a été effectué avec succès.")
        return self.donnees

    def calculer_fragments_total(self):
        """
        Calcule le total des fragments individuels et en contexte.
        """
        if 'Total_Fragments' in self.donnees and 'context_fragments' in self.donnees:
            self.donnees['total_fragments'] = self.donnees['context_fragments'] + self.donnees['Total_Fragments']
        print("Le calcul du total des fragments individuels et en contexte a été effectué avec succès.")
        return self.donnees

    def traiter(self):
        """
        Exécute les fonctions en séquence pour traiter les données.
        """
        self.supprimer_ponctuation()
        self.compter_fragments_contexte()
        self.calculer_fragments_total()
        return self.donnees