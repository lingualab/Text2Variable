class PauseCounter:
    def __init__(self, data, language='English'):
        # Initialisation de l'instance avec les données et la langue spécifiée
        self.data = data
        self.language = language
        self.dictPauses = {
            'English': {
                'filled': ['uhm', 'uh', 'uhummm', 'hum', 'hummmm', 'humm', 'mm', 'mmm', 'Mm', 'um', 'hmmm', 'hmm', 'hm', 'eh', 'err'],
                'empty': ['Pause', 'pause', '...']
            },
            'Francais': {
                'filled': ['euh', 'hum', 'heu', 'hm', 'öhm', 'uhm', 'mmh', 'mh'],
                'empty': ['Pause', 'pause', '...', '...']
            }
        }

    def count_pauses(self):
        """
        Compte le nombre de pauses (remplies et vides) dans les données, en fonction de la langue spécifiée.
        Si la langue n'est pas reconnue, renvoie un message d'erreur.
        """
        # Vérifier si la langue spécifiée est prise en charge
        if self.language not in self.dictPauses:
            return "Langue non reconnue, contactez l'administrateur du programme pour ajouter votre langue."
        
        pause_counts_list = []

        # Essayer de traiter chaque ligne dans la liste des données
        try:
            for line in self.data:
                pause_counts = {'filled': 0, 'empty': 0}
                words = line.split()  # Séparer la ligne en mots
                
                # Compter chaque type de pause dans la ligne
                for word in words:
                    # Normaliser le mot pour la comparaison
                    normalized_word = word.lower()
                    for pause_type, pause_words in self.dictPauses[self.language].items():
                        if normalized_word in pause_words:
                            pause_counts[pause_type] += 1

                pause_counts_list.append(pause_counts)

        except Exception as e:
            # Gérer l'exception en imprimant l'erreur (ou la journaliser ailleurs si nécessaire)
            print(f"Une erreur est survenue : {e}")

        print("Pauses comptées")
        return pause_counts_list
