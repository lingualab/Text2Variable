import math
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import wordnet as wn
import os

def rename_pos_labels(data):
    """
    Renomme les étiquettes POS (parties du discours) de l'anglais vers le français en utilisant une correspondance
    prédéfinie.

    Args:
        data (dict): Un dictionnaire contenant des étiquettes POS comme clés et des informations associées comme valeurs.

    Returns:
        dict: Un nouveau dictionnaire avec les étiquettes POS renommées en français.
    """

    # Correspondance des étiquettes POS entre l'anglais et le français
    pos_mapping = {
        'ADJ': 'Adjectif', 'ADP': 'Preposition', 'ADV': 'Adverbe',
        'AUX': 'Auxiliaire', 'CONJ': 'Conjonction', 'CCONJ': 'Conjonction_de_coordination',
        'DET': 'Determinant', 'INTJ': 'Interjection', 'NOUN': 'Nom',
        'NUM': 'Numeral', 'PART': 'Particule', 'PRON': 'Pronom',
        'PROPN': 'Nom propre', 'PUNCT': 'Ponctuation', 'SCONJ': 'Conjonction_de_subordination',
        'SYM': 'Symbole', 'VERB': 'Verbe', 'X': 'Autre'
    }
    
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

    # Dictionnaire des pronoms déictiques pour chaque langue
    deictic_pronouns = {
        "English": {
            "spatial": {"here", "there", "this", "these", "that", "those"},
            "personal": {"i", "you", "he", "she", "it", "we", "they"},
            "temporal": {"now", "then", "soon", "tomorrow"}
        },
        "Francais": {
            "spatial": {"ce", "cet", "cette", "ces", "celui-ci", "celle-ci", "ceux-ci", "celles-ci", "celui-là", "celle-là", "ceux-là", "celles-là", "y", "en"},
            "personal": {"je", "tu", "il", "elle", "nous", "vous", "ils", "elles"},
            "temporal": {"y", "en"}
        }
    }

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
    # Liste des termes indéfinis en anglais et en français
    termes_indefinis = {
        "Francais": ["truc", "chose", "peu", "beaucoup", "quelques", "plusieurs", "quelqu'un", "tout le monde", 
               "personne", "chacun", "n'importe qui", "autre", "l'autre", "chaque", "ni l'un ni l'autre", 
               "les deux", "d'autres"],
        "English": ["thing", "stuff", "anything", "nothing", "anyone", "one", "either", "neither", "everyone", 
               "no one", "someone", "anybody", "everybody", "nobody", "somebody", "another", "the other", 
               "each", "little", "less", "much", "both", "few", "fewer", "many", "other", "others", "several"]
    }

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






