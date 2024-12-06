import nltk
from nltk.corpus import words
import string
import json
import importlib_resources
from .Database_linguistique import liste_fragments, words_targets
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
        resources = importlib_resources.files(__name__) / "Documents"
        mots_valides = charger_mots_francais(resources / 'french_words.json')
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

    if langue == 'English':
        fragments = liste_fragments[langue]
        for fragment in fragments:
            eventCount += texte.count(fragment)
        
    elif langue == 'Francais':
        print("Le français n'est pas encore supporté.")
        return None
        
    else:
        print("Langue non reconnue pour le moment.")
        return None
    
    return eventCount

def context_fragments(text, language, nlp):
    """
    Cette fonction compte les fragments contextuels dans un texte en fonction de la langue spécifiée.

    Args:
        text (str): Le texte à analyser.
        language (str): La langue du texte (par exemple, "fr" pour le français, "en" pour l'anglais).
        nlp: Le modèle de tokenization spécifique à la langue.

    Returns:
        int: Le nombre de fragments contextuels trouvés dans le texte.
    """

    # Vérifiez si la langue est prise en charge
    if language not in words_targets:
        # Si la langue spécifiée n'est pas dans la liste des langues prises en charge
        print(f"Langue '{language}' non prise en charge.")
        return 0

    # Récupérez les mots cibles à partir du dictionnaire
    words_target = words_targets[language]

    # Tokenize le texte en fonction de la langue
    tokens = [token.text for token in nlp(text)]

    # Initialisez une liste pour stocker les paires de mots consécutives
    combs = []

    # Parcourez les tokens pour créer des paires de mots consécutives
    for token_comb in zip(tokens, tokens[1:]):
        combs.append(token_comb)

    # Comptez combien de paires de mots consécutives correspondent aux mots cibles
    count = sum(f in words_target for f in combs)

    # Retournez le nombre de fragments contextuels trouvés
    return count



