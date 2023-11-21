import spacy

def rename_pos_labels(data):
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

def indice_de_Brunet(Nombre_total_de_mots, Nombre_de_mots_uniques):
    Brunet_indice = Nombre_total_de_mots / (Nombre_de_mots_uniques ** (-0.165)) # Valeur de la constante = -0.165 selon la thèse de Slegers_Antoine_2021
    return Brunet_indice






