import re

class TranscriptionCleaner:
    def __init__(self, data):
        # Initialise l'objet TranscriptionCleaner avec les données à nettoyer.
        self.data = data

    @staticmethod
    def remove_square_brackets(row):
        # Supprime le contenu entre crochets ([...]) en utilisant des expressions régulières.
        cleaned_row = re.sub(r"\[.*?\]", "", row)
        return cleaned_row 

    @staticmethod
    def rem_punct_trans(row):
        # Supprime la ponctuation de la chaîne de caractères, en conservant les lettres, les apostrophes, les espaces, les points et les points d'interrogation.
        trans_no_punct = re.sub(r"[^\w\’ \.\?]", "", row)
        return trans_no_punct

    @staticmethod
    def rem_extra_dots(row):
        # Supprime les points qui suivent un espace dans la chaîne de caractères.
        no_extra = re.sub(r"\s\.", "", row)
        return no_extra

    @staticmethod
    def rem_extra_spaces(row):
        # Remplace deux espaces consécutifs par un seul espace dans la chaîne de caractères.
        no_extra_spaces = re.sub(r"\s\s", " ", row)
        return no_extra_spaces
    
    def apply_cleaning_functions(self):
        if isinstance(self.data, list):
            # Si self.data est une liste de chaînes de caractères, applique les fonctions de nettoyage à chaque élément.
            cleaned_data = [self.remove_square_brackets(row) for row in self.data]
            cleaned_data = [self.rem_punct_trans(row) for row in cleaned_data]
            cleaned_data = [self.rem_extra_dots(row) for row in cleaned_data]
            cleaned_data = [self.rem_extra_spaces(row) for row in cleaned_data]
            print("Transcriptions nettoyées. Modifications apportées : "
                  "\n1. Suppression du contenu entre crochets."
                  "\n2. Suppression de la ponctuation sauf les lettres, les apostrophes, les points et les points d'interrogation."
                  "\n3. Suppression des points suivant un espace."
                  "\n4. Remplacement des espaces consécutifs par un seul espace.")
            # Joint les éléments nettoyés de la liste en une seule chaîne de caractères.
            unified_text = ' '.join(cleaned_data)
            return unified_text
        else:
            print("Erreur : L'entrée doit être une liste de chaînes de caractères.")
            return None
