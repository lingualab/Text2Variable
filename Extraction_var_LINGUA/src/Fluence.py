from collections import Counter
import re

def pauses_silencieuses(texte, langue):
    """
    Compte le nombre total d'occurrences de "[pause]" dans le texte, selon la langue spécifiée.
    
    Args:
    texte (str): Le texte à analyser.
    langue (str): La langue du texte ('English' ou 'Francais').
    
    Returns:
    int: Le nombre d'occurrences de pauses silencieuses.
    """
    if langue == 'English':
        key_word = '[break]'
    elif langue == 'Francais':
        key_word = '[pause]'
    else:
        print("Langue non reconnue pour le moment.")
        return None
    
    return texte.count(key_word)


def pauses_remplies(texte, langue):
    """
    Compte le nombre total d'occurrences des mots spécifiés dans le texte, selon la langue.

    Args:
    texte (str): Le texte à analyser.
    langue (str): La langue du texte ('English' ou 'Francais').

    Returns:
    int: Le nombre d'occurrences des pauses remplies ou -1 si la langue n'est pas prise en charge.
    """
    dictPauses = {
        'English': {
            'filled': ['uhm', 'uh', 'uhummm', 'hum', 'hummmm', 'humm', 'mm', 'mmm', 'Mm', 'um', 'hmmm', 'hmm', 'hm', 'eh', 'err']
        },
        'Francais': {
            'filled': ['euh', 'hum', 'heu', 'hm', 'öhm', 'uhm', 'mmh', 'mh']
        }
    }

    if langue in dictPauses:
        filled_pauses = dictPauses[langue]['filled']
        count = sum(texte.count(pause) for pause in filled_pauses)
        return count
    else:
        return -1  # Retourne -1 pour indiquer que la langue n'est pas prise en charge.

def nombre_repetition_mot(lemmes):
    """
    Compte le nombre de lemmes différents et le nombre de répétitions dans une liste de lemmes.

    Args:
    lemmes (list): Une liste de lemmes.

    Returns:
    tuple: Un tuple contenant le nombre de lemmes différents et le nombre de répétitions.
    """
    # Compte le nombre de lemmes différents
    nombre_lemmes_differents = len(set(lemmes))
    
    # Compte le nombre total de mots
    nombre_total_mots = len(lemmes)
    
    # Calcule le nombre de répétitions
    nombre_repetitions = nombre_total_mots - nombre_lemmes_differents
    
    return nombre_lemmes_differents, nombre_repetitions