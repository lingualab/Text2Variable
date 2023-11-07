from lexicalrichness import LexicalRichness
import numpy as np

class AnalyseurLemmesUniques:
    def __init__(self, donnees):
        self.donnees = donnees

    def _unique_iter(self, iterable):
        return set(iterable)  # Pour un seul participant, nous pouvons directement retourner un ensemble

    def calculer_lemmes_uniques(self):
        lemmes_uniques = self._unique_iter(self.donnees['lemmatized'])
        self.donnees['lemmesUniques'] = len(lemmes_uniques)
        print("Lemmes uniques calculés.")
        return self.donnees

class StatsHonoreBrunet:
    def __init__(self, donnees):
        self.donnees = donnees

    def calculer_Honore_et_Brunet(self):
        types = self.donnees['Nombre_types_mots']
        lemmes_uniques = self.donnees['lemmesUniques']
        tokens = self.donnees['Nombre_tokens_mots']

        honore = 100 * np.log(types) / (1 - (lemmes_uniques / tokens))
        brunet = types ** (tokens ** -0.165)

        self.donnees['Honore'] = honore
        self.donnees['Brunet'] = brunet
        print("Statistiques d'Honoré et de Brunet calculées.")
        return self.donnees

class AnalyseurMATTR:
    def __init__(self, donnees):
        self.donnees = donnees

    def get_MATTR(self, texte):
        tailles_fenetres = [10, 25, 40]
        lex = LexicalRichness(' '.join(texte))
        return [lex.mattr(taille_fenetre) for taille_fenetre in tailles_fenetres]

    def calculer_MATTR(self):
        valeurs_mattr = self.get_MATTR(self.donnees['tokenizedClean'])
        
        self.donnees['MATTR_10'] = valeurs_mattr[0]
        self.donnees['MATTR_25'] = valeurs_mattr[1]
        self.donnees['MATTR_40'] = valeurs_mattr[2]

        print("MATTR calculé pour différentes tailles de fenêtres.")
        return self.donnees




