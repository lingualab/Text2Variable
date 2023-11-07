class CompteurDeFragments:
    def __init__(self, langue, data):
        # Initialise la classe avec les données fournies et un dictionnaire de fragments à compter.
        self.langue = langue
        self.data = data
        self.dict_fragments = {
            'English': ['f', 'n', 'N', 'di', 'wa', 'dr', 'clo', 'di', 'lo', 'b', 'mo', 'wat', 'gon', 'tw', 'wha', 'st', 'rec', 'fff', 'ha', 'i',
                        'hap', 'gir', 'mirr', 'gra', 'ba', 'sh', 'r', 'fa', 'ben', 'ch', 'ru', 'chil', 'd', 'ap', 's', 'laun'],
            'Francais': ['e', 'le', 'la', 'un', 'une', 'du', 'de', 'la', 'et', 'ou', 'mais', 'par', 'pour', 'dans', 'sur', 'sous', 'entre', 'avec',
                         'elle', 'il', 'les', 'des', 'que', 'qui', 'quoi', 'où', 'si', 'ce', 'ça', 'cela', 'cet', 'cette', 'plus', 'moins', 'aussi']
        }  # La liste francaise est fausse, c'est une imaginaire pour tester le code !

    def compter(self):
        """
        Compte le nombre d'occurrences de chaque fragment dans les données en fonction de la langue.

        Sélectionne la liste de fragments appropriée basée sur la langue, puis compte le nombre
        d'occurrences de chaque fragment dans le texte fourni.
        Les résultats sont stockés dans un dictionnaire.

        Returns:
            dict: Un dictionnaire avec le nombre d'occurrences pour chaque fragment.
        """
        comptage = {}
        total_fragments = 0  # Initialisation du total des fragments comptés
        fragments = self.dict_fragments.get(self.langue, [])

        if not fragments:
            print(f"Aucune liste de fragments trouvée pour la langue '{self.langue}'.")
            return comptage, total_fragments

        for fragment in fragments:
            comptage[fragment] = self.data.count(fragment)
            total_fragments += comptage[fragment]  # Ajout au total

        # Affiche le message de confirmation
        print(f"Le comptage des fragments a été effectué avec succès en {self.langue}.")
        print("Les fragments suivants ont été comptés :", ", ".join(fragments))
        print(f"Total des fragments comptés : {total_fragments}")

        return comptage, total_fragments



