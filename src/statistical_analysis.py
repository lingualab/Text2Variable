class AnalyseTextuelle:
    def __init__(self, texte):
        # Initialise la classe avec le texte à analyser.
        self.texte = texte
        self.resultat = {}

    def analyser(self):
        """
        Effectue une analyse statistique du texte.

        Cette méthode calcule la longueur moyenne des mots et compte le nombre de types (mots uniques) et le nombre total de tokens (mots).

        Returns:
            dict: Un dictionnaire contenant les résultats de l'analyse.
        """
        # Appelle les méthodes pour effectuer l'analyse.
        self.resultat['longueur_moyenne_mots'] = self.calculer_longueur_moyenne_mots()
        self.resultat['nombre_types'], self.resultat['nombre_tokens'] = self.compter_types_tokens()

        # Affiche un message de confirmation avec une description des statistiques calculées.
        print("L'analyse textuelle a été effectuée avec succès.")
        print(f"Statistiques calculées: longueur moyenne des mots, nombre de types, nombre de tokens.")

        return self.resultat

    def calculer_longueur_moyenne_mots(self):
        """
        Calcule la longueur moyenne des mots dans le texte.

        Returns:
            float: La longueur moyenne des mots dans le texte.
        """
        mots = self.texte.split()  # Divise le texte en mots
        longueur_totale = sum(len(mot) for mot in mots)  # Calcule la longueur totale des mots
        longueur_moyenne = longueur_totale / len(mots) if mots else 0  # Calcule la longueur moyenne
        print(f"La longueur moyenne des mots est de {longueur_moyenne:.2f} caractères.")
        return longueur_moyenne

    def compter_types_tokens(self):
        """
        Compte les types (mots uniques) et les tokens (mots) dans le texte.

        Returns:
            tuple: Le nombre de types et le nombre de tokens dans le texte.
        """
        mots = self.texte.split()  # Divise le texte en mots
        types = set(mots)  # Utilise un ensemble pour trouver les mots uniques
        nombre_types = len(types)
        nombre_tokens = len(mots)
        print(f"Nombre de types (mots uniques) : {nombre_types}")
        print(f"Nombre de tokens (mots) : {nombre_tokens}")
        return nombre_types, nombre_tokens


