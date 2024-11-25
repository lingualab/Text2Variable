import math
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import wordnet as wn
import os
from .Database_linguistique import pos_mapping, deictic_pronouns, termes_indefinis

def rename_pos_labels(data):
    """
    Renomme les étiquettes POS (parties du discours) de l'anglais vers le français en utilisant une correspondance
    prédéfinie.

    Args:
        data (dict): Un dictionnaire contenant des étiquettes POS comme clés et des informations associées comme valeurs.

    Returns:
        dict: Un nouveau dictionnaire avec les étiquettes POS renommées en français.
    """

    # Crée un nouveau dictionnaire avec les étiquettes renommées
    renamed_data = {}
    for pos, info in data.items():
        if pos in pos_mapping:
            renamed_data[pos_mapping[pos]] = info
        else:
            renamed_data[pos] = info
    
    return renamed_data

def Parts_of_Speech(text, nlp):
    """
    Analyse les parties du discours (POS) dans un texte en utilisant un modèle Spacy donné.

    :param text: Texte à analyser
    :param nlp: Modèle Spacy chargé
    :return: Dictionnaire avec les comptes et pourcentages de chaque classe grammaticale
    """
    # Traitement du texte
    doc = nlp(text)

    # Comptage des parties du discours
    pos_counts = {}
    for token in doc:
        pos = token.pos_
        pos_counts[pos] = pos_counts.get(pos, 0) + 1

    # Calcul du nombre total de mots
    total_words = len(doc)

    # Calculer les occurrences en nombre absolu et en pourcentage
    results = {pos: {'count': count, 'percentage': (count / total_words) * 100} for pos, count in pos_counts.items()}

    return rename_pos_labels(results)

def count_open_closed_class_words(text, nlp):
    """
    Compte le nombre de mots des classes ouvertes et fermées dans un texte analysé avec le modèle SpaCy.

    Args:
        text (str): Le texte à analyser.
        nlp (spacy.language.Language): Le modèle de traitement de texte SpaCy.

    Returns:
        tuple: Un tuple contenant le nombre de mots des classes ouvertes (open class) et fermées (closed class).
    """
    # Analyser le texte avec le modèle Spacy
    doc = nlp(text)

    # Catégories de classes ouvertes et fermées
    open_classes = ['NOUN', 'VERB', 'ADJ', 'ADV']
    closed_classes = ['CONJ', 'PRON', 'DET', 'ADP']

    # Comptage
    open_class_count = 0
    closed_class_count = 0

    for token in doc:
        if token.pos_ in open_classes:
            open_class_count += 1
        elif token.pos_ in closed_classes:
            closed_class_count += 1

    return open_class_count, closed_class_count

def compter_verbes_conjugues(texte, langue, nlp):
    """
    Compte le nombre de verbes conjugués dans un texte donné.
    
    Args:
    texte (str): Le texte à analyser.
    langue (str): La langue du texte ('English' ou 'Francais').
    modele (str): Le modèle spaCy à utiliser pour l'analyse.

    Returns:
    int: Le nombre de verbes conjugués.
    """
    if langue not in ['English', 'Francais']:
        return "Langue non prise en charge. Veuillez choisir 'English' ou 'Francais'."

    doc = nlp(texte)

    # Comptage des verbes conjugués (en excluant la forme de base)
    nombre_verbes = sum(1 for token in doc if token.pos_ == 'VERB' and token.tag_ != 'VB')
    return nombre_verbes

def compter_gerondifs(texte, langue, nlp):
    """
    Compte le nombre de gérondifs dans un texte donné.
    
    Args:
    texte (str): Le texte à analyser.
    langue (str): La langue du texte ('English' ou 'Francais').
    modele (str): Le modèle spaCy à utiliser pour l'analyse.

    Returns:
    int: Le nombre de gérondifs.
    """
    if langue not in ['English', 'Francais']:
        return "Langue non prise en charge. Veuillez choisir 'English' ou 'Francais'."

    doc = nlp(texte)

    # Comptage des gérondifs (en anglais, étiquetés comme 'VBG')
    nombre_gerondifs = sum(1 for token in doc if token.tag_ == 'VBG')
    return nombre_gerondifs

def calculer_ratios(total_verbes, total_noms, total_pronoms, verbes_inflexion, mots_classe_ouverte, mots_classe_fermee, gerondifs, total_mots):
    """
    Calcule les ratios suivants:
    - Pronoms/Noms + Pronoms
    - Noms/Noms + Pronoms
    - Noms/Noms + Verbes
    - Verbes/Noms + Verbes
    - Verbes avec inflexions/Total Verbes
    - Mots de classe ouverte/Total Mots
    - Mots de classe fermée/Total Mots
    - Gérondifs/Total Verbes
    - Gérondifs/Total Mots
    """
    # Calcul des ratios
    ratios = {
        'Pronoms/(Noms+Pronoms)': total_pronoms / (total_noms + total_pronoms) if (total_noms + total_pronoms) > 0 else 'N/A',
        'Noms/(Noms+Pronoms)': total_noms / (total_noms + total_pronoms) if (total_noms + total_pronoms) > 0 else 'N/A',
        'Noms/(Noms+Verbes)': total_noms / (total_noms + total_verbes) if (total_noms + total_verbes) > 0 else 'N/A',
        'Verbes/(Noms+Verbes)': total_verbes / (total_noms + total_verbes) if (total_noms + total_verbes) > 0 else 'N/A',
        'Verbes_avec_inflexions/Total_Verbes': verbes_inflexion / total_verbes if total_verbes > 0 else 'N/A',
        'Mots_de_classe_ouverte/Total_Mots': mots_classe_ouverte / total_mots if total_mots > 0 else 'N/A',
        'Mots_de_classe_fermee/Total_Mots': mots_classe_fermee / total_mots if total_mots > 0 else 'N/A',
        'Gerondifs/Total_Verbes': gerondifs / total_verbes if total_verbes > 0 else 'N/A',
        'Gerondifs/Total_Mots': gerondifs / total_mots if total_mots > 0 else 'N/A'
    }

    return ratios

def count_light_verbs(text, langue, nlp):
    """
    Compte le nombre d'occurrences de verbes légers dans un texte.

    :param text: Texte à analyser
    :param light_verbs: Liste des verbes légers
    :param nlp: Modèle Spacy chargé
    :return: Nombre d'occurrences des verbes légers, proportion par rapport au total des verbes
    """

    return None, None


def count_deictic_pronouns(text, language, nlp_model):
    """
    Compte les pronoms déictiques dans un texte en anglais ou en français.

    Args:
    - text (str): Le texte à analyser.
    - language (str): La langue du texte ("fr" pour le français, "en" pour l'anglais).
    - nlp_model (spaCy model): Le modèle de langue spaCy.

    Returns:
    - dict: Un dictionnaire avec les comptes des pronoms spatiaux, personnels, temporels et le total.
    """

    if language not in deictic_pronouns:
        raise ValueError("Langue non prise en charge. Choisissez 'en' pour l'anglais ou 'fr' pour le français.")

    # Sélection des ensembles de pronoms selon la langue
    pronouns = deictic_pronouns[language]

    # Traitement du texte avec le modèle spaCy
    doc = nlp_model(text.lower())

    # Comptage des occurrences de chaque catégorie de pronom
    spatial_count = sum(token.text in pronouns["spatial"] for token in doc)
    personal_count = sum(token.text in pronouns["personal"] for token in doc)
    temporal_count = sum(token.text in pronouns["temporal"] for token in doc)
    total_count = spatial_count + personal_count + temporal_count

    return {
        "spatial": spatial_count,
        "personal": personal_count,
        "temporal": temporal_count,
        "total_deictic_pronouns": total_count
    }

def compter_termes_indefinis(texte, langue, nlp):
    """
    Compte le nombre de termes indéfinis dans un texte en fonction de la langue.

    Args:
        texte (str): Le texte à analyser.
        langue (str): La langue du texte ("Francais" ou "English").
        nlp (spacy.language.Language): Le modèle de traitement de texte SpaCy.

    Returns:
        int: Le nombre de termes indéfinis trouvés dans le texte.
    """

    # Tokeniser le texte
    doc = nlp(texte)

    # Compter les occurrences
    compte = sum(token.text in termes_indefinis[langue] for token in doc)

    return compte

def ratio_termes_indefinis(texte, langue, nlp):
    """
    Calcule le ratio de termes indéfinis dans un texte en fonction de la langue.

    Args:
        texte (str): Le texte à analyser.
        langue (str): La langue du texte ("Francais" ou "English").
        nlp (spacy.language.Language): Le modèle de traitement de texte SpaCy.

    Returns:
        tuple: Un tuple contenant le ratio de termes indéfinis par rapport au nombre total de mots
               et le nombre total de termes indéfinis trouvés dans le texte.
    """
    doc = nlp(texte)

    # Nombre total de mots
    total_mots = len([token for token in doc if token.is_alpha])

    # Appel de la fonction de comptage
    compte_indefinis = compter_termes_indefinis(texte, langue, nlp)

    # Calcul du ratio
    ratio = compte_indefinis / total_mots if total_mots > 0 else 0

    return ratio, compte_indefinis

def calculer_mattr(texte, taille_fenetre, nlp):
    """
    Calcule le MATTR (Moving-Average Type-Token Ratio) d'un texte donné en utilisant une fenêtre de taille spécifiée.

    Args:
        texte (str): Le texte à analyser.
        taille_fenetre (int): La taille de la fenêtre de texte à utiliser.
        modele_spacy (str): Le modèle SpaCy à utiliser pour la tokenisation (par exemple, "fr" pour le français).

    Returns:
        float: La valeur MATTR calculée pour le texte.
    """

    # Tokeniser le texte
    tokens = [token.text for token in nlp(texte) if token.is_alpha]

    # Calculer le TTR (Type-Token Ratio) pour chaque fenêtre
    ttr_valeurs = []
    for i in range(len(tokens) - taille_fenetre + 1):
        fenetre = tokens[i:i + taille_fenetre]
        types = set(fenetre)
        ttr = len(types) / len(fenetre)
        ttr_valeurs.append(ttr)

    # Calculer le MATTR (Moving-Average Type-Token Ratio)
    mattr = sum(ttr_valeurs) / len(ttr_valeurs) if ttr_valeurs else 0

    return mattr

def calculer_nbres_mots_unique(texte):
    """
    Calcule le nombre de mots uniques dans un texte donné.

    Args:
        texte (str): Le texte à analyser.

    Returns:
        int: Le nombre de mots uniques dans le texte.
    """
    # Tokeniser le texte en mots
    mots = texte.split()

    # Créer un ensemble pour stocker les mots uniques
    mots_uniques = set(mots)

    # Retourner le nombre de mots uniques
    return len(mots_uniques)

def stat_R_Honore(nbre_mots, nbre_lemmes_different, nbres_mots_unique):
    """
    Calcule la statistique R de Honore pour un texte donné.

    Args:
        nbre_mots (int): Le nombre total de mots dans le texte.
        nbre_lemmes_different (int): Le nombre de types uniques dans le texte.
        nbres_mots_unique (int): Le nombre de types qui n'apparaissent qu'une seule fois dans le texte.

    Returns:
        float: La valeur de la statistique R de Honore.
        
    """
    # Formule de la statistique R de Honore : R=100×log(N)/(1−(V1/V))
    R = 100 * math.log(nbre_mots) / (1 - (nbres_mots_unique / nbre_lemmes_different))
    return R

def indice_de_Brunet(Nombre_total_de_mots, Nombre_de_mots_uniques):
    """
    Calcule l'indice de Brunet, une mesure de diversité lexicale reliant la longueur de l’échantillon au nombre de mots
    différents utilisés dans celui-ci.

    Args:
        Nombre_total_de_mots (int): Le nombre total de mots dans le texte (compte de tokens).
        Nombre_de_mots_uniques (int): Le nombre total de mots uniques dans le texte (compte de types).

    Returns:
        float: L'indice de Brunet calculé.

    Formulaire:
        L'indice de Brunet (W) est calculé selon la formule : W = N ^ (V ^ (-0.165))

    où :
        W (float): L'indice W de Brunet.
        N (int): Le nombre total de mots dans le texte.
        V (int): Le nombre total de mots uniques dans le texte.

    L'indice de Brunet mesure la diversité lexicale d'un texte, indiquant comment la longueur de l'échantillon
    est liée au nombre de mots différents utilisés. Plus l'indice est élevé, plus le texte est diversifié en termes
    de vocabulaire.
    """
    Brunet_indice = Nombre_total_de_mots / (Nombre_de_mots_uniques ** (-0.165))  # Valeur de la constante = -0.165 selon la thèse de Slegers_Antoine_2021
    return Brunet_indice

def analyser_texte(texte, modele_spacy):
    """
    Analyse un texte à l'aide d'un modèle spaCy pour extraire des informations sur les mots, noms, verbes et adjectifs.

    Args:
        texte (str): Le texte à analyser.
        modele_spacy (spacy.language.Language): Le modèle spaCy à utiliser pour l'analyse.

    Returns:
        tuple: Un tuple contenant quatre listes - mots, noms, verbes et adjectifs - extraits du texte.

    Cette fonction prend en entrée un texte et un modèle spaCy. Elle analyse le texte en utilisant le modèle spaCy et extrait les mots
    qui ne sont ni des arrêts (stop words) ni de la ponctuation. Les mots sont stockés dans la liste 'mots'. Les noms (substantifs) sont
    stockés dans la liste 'noms', les verbes dans 'verbes' et les adjectifs dans 'adjectifs'. La fonction retourne un tuple contenant
    ces quatre listes.
    """
    doc = modele_spacy(texte)
    mots, noms, verbes, adjectifs = [], [], [], []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            mots.append(token.text)
            if token.pos_ == 'NOUN':
                noms.append(token.text)
            elif token.pos_ == 'VERB':
                verbes.append(token.text)
            elif token.pos_ == 'ADJ':
                adjectifs.append(token.text)
    return mots, noms, verbes, adjectifs

def calculer_frequence_moyenne(mots, base_de_donnees, colonne_frequence='SUBTLWF'):
    """
    Calcule la fréquence moyenne des mots dans une liste à partir d'une base de données de fréquence.

    Args:
        mots (list): Une liste de mots à partir desquels la fréquence moyenne sera calculée.
        base_de_donnees (pandas.DataFrame): Le DataFrame contenant la base de données de fréquence des mots.
        colonne_frequence (str): Le nom de la colonne dans la base de données contenant les fréquences (par défaut : 'SUBTLWF').

    Returns:
        float: La fréquence moyenne des mots dans la liste, ou 0 si la liste est vide.

    Cette fonction prend en entrée une liste de mots, une base de données de fréquence des mots sous forme de DataFrame et le nom de
    la colonne contenant les fréquences dans la base de données. Elle calcule la fréquence moyenne des mots présents dans la liste en
    recherchant chaque mot dans la base de données et en calculant la moyenne des fréquences correspondantes. Le résultat est renvoyé
    sous forme de nombre flottant.
    """
    somme_frequence = 0
    for mot in mots:
        if mot in base_de_donnees['Word'].values:
            somme_frequence += base_de_donnees[base_de_donnees['Word'] == mot][colonne_frequence].iloc[0]
    return float(somme_frequence / len(mots)) if mots else 0

def calculer_familiarite_moyenne(mots, base_de_donnees):
    """
    Calcule la familiarité moyenne des mots dans une liste à partir d'une base de données de familiarité.

    Args:
        mots (list): Une liste de mots à partir desquels la familiarité moyenne sera calculée.
        base_de_donnees (pandas.DataFrame): Le DataFrame contenant la base de données de familiarité des mots.

    Returns:
        float: La familiarité moyenne des mots dans la liste, ou 0 si la liste est vide ou aucun mot n'a de valeur de familiarité valide.

    Cette fonction prend en entrée une liste de mots et une base de données de familiarité des mots sous forme de DataFrame.
    Elle calcule la familiarité moyenne des mots présents dans la liste en recherchant chaque mot dans la base de données et en calculant la moyenne des valeurs de familiarité correspondantes. Le résultat est renvoyé sous forme de nombre flottant.
    Si aucun mot de la liste n'a de valeur de familiarité valide dans la base de données, la fonction renvoie 0.
    """
    total_familiarite, compteur = 0.0, 0
    for mot in mots:
        if mot in base_de_donnees.index:
            valeur_fam = base_de_donnees.loc[mot, 'FAM']
            try:
                # Convertir la valeur en float
                valeur_fam = float(valeur_fam)
                total_familiarite += valeur_fam
                compteur += 1
            except ValueError:
                # Ignorer si la valeur n'est pas convertible en float
                pass
    return total_familiarite / compteur if compteur > 0 else 0

def calculer_concretude_moyenne(mots, base_de_donnees):
    """
    Calcule la concretude moyenne des mots dans une liste à partir d'une base de données de concretude.

    Args:
        mots (list): Une liste de mots à partir desquels la concretude moyenne sera calculée.
        base_de_donnees (pandas.DataFrame): Le DataFrame contenant la base de données de concretude des mots.

    Returns:
        float: La concretude moyenne des mots dans la liste, ou 0 si la liste est vide ou aucun mot n'a de valeur de concretude valide.

    Cette fonction prend en entrée une liste de mots et une base de données de concretude des mots sous forme de DataFrame.
    Elle calcule la concretude moyenne des mots présents dans la liste en recherchant chaque mot dans la base de données et en calculant la moyenne des valeurs de concretude correspondantes. Le résultat est renvoyé sous forme de nombre flottant.
    Si aucun mot de la liste n'a de valeur de concretude valide dans la base de données, la fonction renvoie 0.
    """
    total_concretude, compteur = 0.0, 0
    for mot in mots:
        if mot in base_de_donnees.index:
            valeur_concretude = base_de_donnees.loc[mot, 'Conc.M']
            if not pd.isna(valeur_concretude):
                total_concretude += valeur_concretude
                compteur += 1
    return float(total_concretude / compteur) if compteur > 0 else 0

def calculer_valence_moyenne(mots, base_de_donnees):
    """
    Calcule la valence moyenne des mots dans une liste à partir d'une base de données de valence.

    Args:
        mots (list): Une liste de mots à partir desquels la valence moyenne sera calculée.
        base_de_donnees (pandas.DataFrame): Le DataFrame contenant la base de données de valence des mots.

    Returns:
        float: La valence moyenne des mots dans la liste, ou 0 si la liste est vide ou aucun mot n'a de valeur de valence valide.

    Cette fonction prend en entrée une liste de mots et une base de données de valence des mots sous forme de DataFrame.
    Elle calcule la valence moyenne des mots présents dans la liste en recherchant chaque mot dans la base de données et en calculant la moyenne des valeurs de valence correspondantes. Le résultat est renvoyé sous forme de nombre flottant.
    Si aucun mot de la liste n'a de valeur de valence valide dans la base de données, la fonction renvoie 0.
    """
    total_valence, compteur = 0.0, 0
    for mot in mots:
        if mot in base_de_donnees.index:
            valeur_valence = base_de_donnees.loc[mot, 'V.Mean.Sum']
            if not pd.isna(valeur_valence):
                total_valence += valeur_valence
                compteur += 1
    return float(total_valence / compteur) if compteur > 0 else 0

def calculer_imageabilite_moyenne(mots, base_de_donnees):
    """
    Calcule l'imageabilité moyenne des mots dans une liste à partir d'une base de données d'imageabilité.

    Args:
        mots (list): Une liste de mots à partir desquels l'imageabilité moyenne sera calculée.
        base_de_donnees (pandas.DataFrame): Le DataFrame contenant la base de données d'imageabilité des mots.

    Returns:
        float: L'imageabilité moyenne des mots dans la liste, ou 0 si la liste est vide ou aucun mot n'a de valeur d'imageabilité valide.

    Cette fonction prend en entrée une liste de mots et une base de données d'imageabilité des mots sous forme de DataFrame.
    Elle calcule l'imageabilité moyenne des mots présents dans la liste en recherchant chaque mot dans la base de données et en calculant la moyenne des valeurs d'imageabilité correspondantes. Le résultat est renvoyé sous forme de nombre flottant.
    Si aucun mot de la liste n'a de valeur d'imageabilité valide dans la base de données, la fonction renvoie 0.
    """
    total_imageabilite, compteur = 0.0, 0
    for mot in mots:
        if mot in base_de_donnees.index:
            valeur_imageabilite = base_de_donnees.loc[mot, 'IMAG']
            try:
                # Convertir la valeur en float
                valeur_imageabilite = float(valeur_imageabilite)
                total_imageabilite += valeur_imageabilite
                compteur += 1
            except ValueError:
                # Ignorer si la valeur n'est pas convertible en float
                pass
    return total_imageabilite / compteur if compteur > 0 else 0
