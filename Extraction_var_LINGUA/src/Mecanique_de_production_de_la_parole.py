import nltk
from nltk.corpus import words
import string
import json

# Téléchargement des listes de mots pour l'anglais a faire la premiere fois
#nltk.download('words')

def charger_mots_francais(chemin_fichier):
    """
    Charge une liste de mots français à partir d'un fichier JSON.

    Args:
    chemin_fichier (str): Le chemin du fichier contenant les mots français.

    Returns:
    set: Un ensemble de mots français.
    """
    # Ouvre le fichier spécifié en mode lecture ('r') avec un encodage UTF-8
    with open(chemin_fichier, 'r', encoding='utf-8') as file:
        # Charge les données depuis le fichier JSON et les convertit en ensemble (set) pour une recherche rapide
        mots_francais = set(json.load(file))

    return mots_francais  # Retourne l'ensemble des mots français

def compter_lemmes(liste_mots):
    """
    Compte le nombre de mots dans une liste, en excluant la ponctuation.

    Args:
    liste_mots (list): La liste des mots, y compris la ponctuation.

    Returns:
    int: Le nombre de mots après l'exclusion de la ponctuation.
    """
    mots_sans_ponctuation = [mot for mot in liste_mots if mot not in string.punctuation]
    return len(mots_sans_ponctuation)

def identification_fragments(tokens, langue):
    """
    Identifie les fragments de mots dans une liste de tokens.

    Args:
    tokens (list): La liste des tokens.
    langue (str): La langue des tokens ('english' ou 'francais').

    Returns:
    list: Une liste des fragments de mots identifiés.
    """
    if langue == 'English':
        # Dictionnaire de mots anglais
        mots_valides = set(words.words())
    elif langue == 'Francais':
        # Utilisation de la liste des mots français chargée
        chemin_fichier = 'French words.json'
        mots_francais = charger_mots_francais(chemin_fichier)
        mots_valides = mots_francais
    else:
        print("Langue non reconnue pour le moment.")
        return None

    # Identification des fragments
    fragments = [token for token in tokens if token.lower() not in mots_valides]
    
    return fragments

def compteur_fragments(tokens, langue, print_fragments=False):
    """
    Compte le nombre de fragments dans une liste de tokens.

    Args:
    tokens (list): La liste des tokens.
    langue (str): La langue des tokens ('english' ou 'francais').
    print_fragments (bool): Si vrai, affiche les fragments trouvés.

    Returns:
    int: Le nombre de fragments de mots.
    """
    fragments = identification_fragments(tokens, langue)
    if print_fragments == True:
        print(fragments)
    
    if fragments is None:
        return None
    else:
        return len(fragments)

def compteur_fragment_anciennce_version(texte, langue):
    """
    Compte le nombre d'occurrences de fragments spécifiques dans le texte en fonction de la langue.

    Args:
        texte (str): Le texte dans lequel compter les fragments.
        langue (str): La langue du texte ('English' ou 'Francais').

    Returns:
        int: Le nombre d'occurrences de fragments dans le texte. Retourne None si la langue n'est pas reconnue.

    Cette fonction compte le nombre d'occurrences de fragments spécifiques dans un texte en fonction de la langue
    spécifiée ('English' ou 'Francais'). Elle retourne le nombre total d'occurrences de fragments dans le texte.
    Si la langue n'est pas reconnue, la fonction retourne None.
    """
    eventCount = 0
    liste_fragments = ['f', 'n', 'N', 'di', 'wa', 'dr', 'clo', 'di', 'lo', 'b', 'mo', 'wat', 'gon', 'tw', 'wha', 'st', 'rec', 'fff', 'ha', 'i',
                                'hap', 'gir', 'mirr', 'gra', 'ba', 'sh', 'r', 'fa', 'ben', 'ch', 'ru', 'chil', 'd', 'ap', 's', 'laun']
    if langue == 'English':
        for mot in texte:
            if mot in liste_fragments:
                eventCount += 1
        
        
        
    elif langue == 'Francais':
        print("le francais n'est pas encore supporté")
        return None
        
    else:
        print("Langue non reconnue pour le moment.")
        return None
    
    return eventCount

def context_fragments(tokens):
    """
    Compte le nombre de paires de mots spécifiques dans une liste de tokens.

    Args:
        tokens (list): Une liste de tokens.

    Returns:
        int: Le nombre de paires de mots spécifiques trouvées dans la liste de tokens.

    Cette fonction compte le nombre de paires de mots spécifiques dans une liste de tokens en utilisant une liste de
    paires cibles prédéfinies. Elle retourne le nombre total de paires de mots spécifiques trouvées dans la liste
    de tokens.
    """
    words_target = [('the', 'there'), ('dry', 'or'), ('out', 'outside'), ('wash', 'drying'), ('curt', 'the'), ('is', 'spill'), ('wash', 'is'), ('bow', 'Cup'), ('tap', 'taps'),
                   ('spill', 'is'), ('kit', 'the'), ('stand', 'standing'), ('go', 'reaching'), ('dish', 'The'), ('look', 'uh'), ('dry', 'or'), ('watch', 'washing'), ('sleeve', 'sleeveless'),
                   ('cook', 'cookie'), ('a', 'an'), ('day', 'daytime'), ('curt', 'the'), ('look', 'reaching'), ('sister', 'reach'), ('cab', 'the'), ('cook', 'the'), ('stand', 'climbing'), ('her','ask'),
                   ('ask', 'asking'), ('up', 'upper')] 
    combs = []
    for token_comb in more_itertools.windowed(tokens, 2):
        combs.append(token_comb) 
    count = sum(f in words_target for f in combs)
    return count