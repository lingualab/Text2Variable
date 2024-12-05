import itertools
import numpy as np
from .Database_linguistique import dictICU_cookie_fr, dictICU_cookie_en, dictICU_picnic_en

dict_ICUs = {
    "en": {
        "cookie_theft": dictICU_cookie_en,
        "picnic": dictICU_picnic_en,
    },
    "fr": {
        "cookie_theft": dictICU_cookie_fr,
    }
}

def analyse_text(text, language, task):
    """
    Analyse le texte pour détecter la présence d'ICUs (Informations de Contenu Uniques) associées à des sujets,
    lieux, objets et actions spécifiques. Le code est conçu pour être utilisé dans le contexte de l'image "Cookie Theft".
    
    Args:
        text (str): Le texte à analyser.
        language (str): La langue du texte ("Francais" ou "English").
        task (str): image utilisée pour la production du texte ("cookie_theft" ou "picnic").

    Returns:
        dict: Un dictionnaire contenant des informations sur la présence des ICUs. Chaque ICU est associée à une clé
              et la valeur correspondante est True si l'ICU est trouvée dans le texte, sinon False.
    """
    dictICU = dict_ICUs.get(language, {}).get(task, None)

    if not dictICU:
        print("Langue non reconnue pour le moment.")
        return dict()

    # Initialisation du dictionnaire de résultats
    results = {key: False for key in dictICU}

    # Vérification de la présence de chaque ICU dans le texte
    for key, values in dictICU.items():
        for value in values:
            if value in text:
                results[key] = True
                break  # Passe à la clé suivante dès qu'une correspondance est trouvée

    return results

def nombre_ICU(dict_ICUs):
    """
    Calcule le nombre total d'ICUs étiquetées comme "VRAI" dans le dictionnaire donné.

    Args:
    dict_ICUs (dict): Le dictionnaire contenant les ICUs avec leurs étiquettes.

    Returns:
    int: Le nombre total d'ICUs étiquetées comme "VRAI".
    """
    # Initialiser un compteur pour suivre le nombre d'ICUs étiquetées comme "VRAI"
    nombre_VRAI = 0

    # Parcourir le dictionnaire et compter les ICUs étiquetées comme "VRAI"
    for mot, valeur in dict_ICUs.items():
        if valeur:  # Si la valeur est True (VRAI)
            nombre_VRAI += 1

    return nombre_VRAI

def calculer_ratio_mots_par_ICU_VRAI(nombre_total_de_mots, nombre_ICU_VRAI):
    """
    Calcule le ratio de mots par ICU "VRAI".

    Args:
    nombre_total_de_mots (int): Le nombre total de mots dans l'échantillon.
    nombre_ICU_VRAI (int): Le nombre total d'ICUs étiquetées comme "VRAI".

    Returns:
    float: Le ratio de mots par ICU "VRAI".
    """
    if nombre_ICU_VRAI == 0:
        return 0.0  # Éviter une division par zéro
    else:
        ratio = nombre_total_de_mots / nombre_ICU_VRAI
        return ratio

def calculer_similarite(embeddings):
    """
    Calcule la similarité moyenne entre les paires d'embeddings fournis en utilisant le produit scalaire normalisé.

    Args:
        embeddings (list): Une liste d'embeddings (vecteurs) à comparer.

    Returns:
        float: La similarité moyenne entre les paires d'embeddings normalisée entre -1 (dissimilaire) et 1 (similaire).
    """
    similarites = []
    for emb1, emb2 in itertools.combinations(embeddings, 2):
        similarite = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        similarites.append(similarite)
    return np.mean(similarites)

def densite_idees(texte, modele, tailles_fenetres=[3, 10, 25, 40]):
    """
    Calcule la densité d'idées pour différentes tailles de fenêtres dans un texte en utilisant des embeddings
    et la similarité moyenne entre les mots dans ces fenêtres.

    Args:
        texte (str): Le texte à analyser.
        modele (spacy.language.Language): Le modèle de traitement de texte Spacy.
        tailles_fenetres (list): Une liste de tailles de fenêtres à utiliser pour le calcul de densité.

    Returns:
        dict: Un dictionnaire contenant les tailles de fenêtres en tant que clés et la densité d'idées associée
              en tant que valeurs. Les valeurs peuvent être NaN si les moyennes sont indéfinies pour certaines fenêtres.
    """
    doc = modele(texte)
    embeddings = [token.vector for token in doc if not token.is_stop and not token.is_punct]
    resultats = {}

    for taille in tailles_fenetres:
        moyennes = []
        for i in range(0, len(embeddings) - taille + 1, taille // 2):
            fenetre = embeddings[i:i + taille]
            moyenne = calculer_similarite(fenetre)
            moyennes.append(moyenne)
        
        # Vérifiez si moyennes n'est pas vide avant d'appeler np.nanmean()
        if moyennes:
            moyenne_sans_NaN = np.nanmean(moyennes)
        else:
            moyenne_sans_NaN = np.nan  # Ou une autre valeur par défaut si nécessaire
        
        resultats[taille] = moyenne_sans_NaN

    return resultats
