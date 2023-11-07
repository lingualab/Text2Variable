class ProportionalAnalyser:
    def __init__(self, donnees):
        self.donnees = donnees

    def calculer_proportions_POS(self):
        """Calcule les proportions de différentes parties du discours."""
        numWords = self.donnees['Longueur_moyenne_mots']
        
        # Proportions simples
        for key in ['nouns', 'pronouns', 'verbs', 'adjectives', 'adverbs', 'prepositions', 'determiners', 'conjunctions']:
            self.donnees[f'{key}_Proportion'] = self.donnees[key] / numWords

        # Proportions combinées
        proportions = [
            ('nounRatio_nounVerb', 'nouns', ['nouns', 'verbs']),
            ('nounRatio_nounVerbAdj', 'nouns', ['nouns', 'verbs', 'adjectives']),
            ('nounRatio_nounPronoun', 'nouns', ['nouns', 'pronouns']),
            ('verbRatio_noun', 'verbs', ['nouns']),
            ('verbRatio_nounVerb', 'verbs', ['nouns', 'verbs']),
            ('verbRatio_nounVerbAdj', 'verbs', ['nouns', 'verbs', 'adjectives']),
            ('AdjRatio_nounVerb', 'adjectives', ['nouns', 'verbs']),
            ('AdjRatio_nounVerbAdj', 'adjectives', ['nouns', 'verbs', 'adjectives']),
            ('pronounRatio_nounPronoun', 'pronouns', ['nouns', 'pronouns'])
        ]
        
        for prop_name, numerator_key, denominator_keys in proportions:
            denominator = sum(self.donnees[key] for key in denominator_keys)
            self.donnees[prop_name] = self.donnees[numerator_key] / denominator
        
        print("Proportions POS calculées.")

    def calculer_proportions_syntaxe(self):
        """Calcule les proportions de différentes structures syntaxiques."""
        numWords = self.donnees['Longueur_moyenne_mots']

        # Proportions simples
        for key in ['leftChildren', 'rightChildren', 'inflectedVerbs', 'gerunds']:
            self.donnees[f'{key}_total'] = self.donnees[key] / numWords

        # Proportions combinées
        self.donnees['leftChildren_proportion'] = self.donnees['leftChildren'] / (self.donnees['leftChildren'] + self.donnees['rightChildren'])
        self.donnees['rightChildren_proportion'] = self.donnees['rightChildren'] / (self.donnees['leftChildren'] + self.donnees['rightChildren'])
        self.donnees['infl_totalVerbs'] = self.donnees['inflectedVerbs'] / self.donnees['verbs']
        self.donnees['gerundsRatio_verbs'] = self.donnees['gerunds'] / self.donnees['verbs']
        
        print("Proportions syntaxiques calculées.")

    def traiter(self):
        """Méthode principale pour traiter toutes les proportions."""
        self.calculer_proportions_POS()
        self.calculer_proportions_syntaxe()
        print("Analyse proportionnelle terminée.")
        return self.donnees