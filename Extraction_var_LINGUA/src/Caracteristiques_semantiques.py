import itertools
import numpy as np

def analyse_text(text, language):
    """
    Analyse le texte pour détecter la présence d'ICUs (Informations de Contenu Uniques) associées à des sujets,
    lieux, objets et actions spécifiques. Le code est conçu pour être utilisé dans le contexte de l'image "Cookie Theft".
    
    Args:
        text (str): Le texte à analyser.
        language (str): La langue du texte ("Francais" ou "English").

    Returns:
        dict: Un dictionnaire contenant des informations sur la présence des ICUs. Chaque ICU est associée à une clé
              et la valeur correspondante est True si l'ICU est trouvée dans le texte, sinon False.
    """
    # Dictionnaires ICU pour les deux langues
    dictICU_fr = {
        'mère': ['mère', 'maman', 'mamie', 'mam', 'mamma', 'momma', 'ma', 'mama', 'femme'],
        'garçon': ['garçon', 'gamin', 'mec', 'gosse', 'fils', 'écolier', 'jeune homme', 'jeune garçon', 'enfant mâle'],
        'fille': ['fille', 'fille', 'jeune fille', 'écolière', 'jeune dame', 'jeune fille', 'enfant femelle'],
        'cuisine': ['cuisine'],
        'extérieur': ['extérieur', 'dehors', "à l'air libre", 'en plein air'],
        'robinet': ['robinet', 'évacuation', 'mitigeur'],
        'eau': ['eau'],
        'évier': ['évier'],
        'sol': ['sol', 'terre', 'plancher'],
        'assiette': ['assiette', 'plat', 'plateau', 'soucoupe'],
        'vaisselle sur comptoir': ['posée sur', 'placée sur', 'étalée sur'],
        'comptoir': ['comptoir', 'plan de travail'],
        'cookies': ['cookies', 'biscuit', 'biscuits'],
        'bocal': ['bocal', 'pot', 'boîte'],
        'placard': ['placard', 'armoire', 'placards', 'armoires'],
        'tabouret': ['tabouret', 'escabeau'],
        'fenêtre': ['fenêtre'],
        'rideau': ['rideau', 'store', 'écran', 'volet'],
        'garçon prenant cookie': ['prenant', 'saisissant', 'atteignant', 'prendre', 'saisir', 'atteindre', 'se saisir'],
        'garçon/tabouret tombant': ['tombant', 'basculant', 'tomber', 'basculer'],
        'mère séchant/lavant vaisselle': ['sécher', 'séchant', 'laver', 'lavant', 'nettoyer', 'nettoyant', 'frotter', 'frottant', 'essuyant', 'faire la vaisselle'],
        'eau débordant': ['déborder', 'débordant', 'renverser', 'renversant', 'cascader', 'évier débordant', 'débordement'],
        'fille demandant cookie': ['demander', 'demandant', 'vouloir', 'veut', 'solliciter', 'sollicite'],
        'mère indifférente au débordement': ['indifférente', 'pas dérangée', 'se soucier', 'pas dérangé', 'remarqué', 'déranger'],
        'mère ne remarquant pas les enfants': ['inconsciente', 'remarqué', 'pas remarqué', 'pas prendre garde', 'pas dérangée', 'pas dérangé'],
    }

    dictICU_en = {'mother': ['mother', 'mom', 'mum', 'mommy', 'mummy', 'mamma', 'momma', 'ma', 'mama', 'woman'], 
            'boy': ['boy', 'guy', 'dude', 'lad', 'son', 'schoolboy', 'young man', 'son', 'young boy', 'male child'], 
            'girl': ['girl', 'daughter', 'lass', 'schoolgirl', 'young lady', 'young girl', 'female child'],
            'kitchen': ['kitchen'], 
            'exterior': ['exterior', 'outside', 'outdoor', 'outdoors'],
            'faucet': ['faucet', 'drain', 'tap'],
            'water': ['water'], 
            'sink': ['sink'],            
            'floor': ['floor', 'ground', 'flooring'],
            'plate': ['plate', 'dish', 'platter', 'saucer'], 
            'dishes on counter': ['laying on', 'placed on', 'spread on'], 
            'counter' : ['counter', 'worktop', 'counter top', 'countertop'],
            'cookies': ['cookies', 'cookie', 'biscuits', 'biscuit'],
            'jar': ['jar', 'pot', 'tin'], 
            'cabinet': ['cabinet', 'cupboard', 'cabinets', 'cupboards'], 
            'stool': ['stool', 'footstool'], 
            'window': ['window'], 
            'curtain': ['curtain', 'blind', 'screen', 'shutter'], 
            'boy taking cookie': ['taking', 'grabbing', 'reaching', 'take', 'grab', 'reach', 'get hold'], 
            'boy/stool falling': ['falling', 'tipping', 'fall', 'tip'], 
            'mother drying/washing dishes': ['dry', 'drying', 'wash', 'washing', 'clean', 'cleaning', 'scrub', 'scrubbing', 'wiping', 'doing dishes', 'doing the dishes'],
            'water overflowing': ['overflow', 'overflowing', 'spill', 'spilling', 'cascading', 'sink running over', 'overrunning'], 
            'girl asking for cookie': ['ask', 'asking', 'want', 'wants', 'requesting', 'requests'],
            'mother unconcerned about overflowing': ['unconcerned', 'unbothered', 'care', 'not bothered', 'noticed', 'bother'],
            'mother not noticing children': ['unnoticing', 'noticed', 'not noticed', 'not take notice', 'unbothered', 'not bothered'],
    }
    if language == "Francais":
        dictICU = dictICU_fr
    elif language == "English":
        dictICU = dictICU_en
    else:
        print("Langue non reconnue pour le moment.")
        return None


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

def traiter_texte(texte, modele):
    """
    Traite un texte en utilisant un modèle de traitement de texte spécifique pour générer des embeddings (vecteurs) 
    pour chaque token du texte, en excluant les stop words et la ponctuation.

    Args:
        texte (str): Le texte à traiter.
        modele (spacy.language.Language): Le modèle de traitement de texte Spacy.

    Returns:
        list: Une liste d'embeddings (vecteurs) correspondant aux tokens du texte, après avoir exclu les stop words 
              et la ponctuation.
    """
    doc = modele(texte)
    return [token.vector for token in doc if not token.is_stop and not token.is_punct]

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
    embeddings = traiter_texte(texte, modele)
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
