def get_dependency_counts(text, spacy_model):
    """
    Analyse les dépendances syntaxiques d'un texte.
    :param text: Le texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Dictionnaire des dépendances syntaxiques avec leur comptage.
    """
    doc = spacy_model(text)
    dep_counts = {}
    for token in doc:
        dep = token.dep_
        dep_counts[dep] = dep_counts.get(dep, 0) + 1
    return dep_counts

def get_relative_dependency_frequencies(dep_counts, total_words):
    """
    Calcule les fréquences relatives des dépendances syntaxiques.
    :param dep_counts: Dictionnaire des dépendances syntaxiques avec leur comptage.
    :param total_words: Nombre total de mots dans le texte.
    :return: Dictionnaire des dépendances avec leurs fréquences relatives.
    """
    return {dep: count / total_words for dep, count in dep_counts.items()}

def analyze_text_dependencies(text, spacy_model):
    """
    Analyse les dépendances syntaxiques d'un texte dans une langue donnée.
    :param text: Texte à analyser.
    :return: Deux dictionnaires : comptes absolus et fréquences relatives des dépendances.
    """
    
    dep_counts = get_dependency_counts(text, spacy_model)
    total_words = len(text.split())
    relative_freqs = get_relative_dependency_frequencies(dep_counts, total_words)
    return dep_counts, relative_freqs

def add_dependency_info(output_data, dep_absolue, dep_relative):
    """
    Ajoute les informations de dépendance au dictionnaire de données de sortie.

    Args:
        output_data (dict): Le dictionnaire de données de sortie où ajouter les informations de dépendance.
        dep_absolue (dict): Un dictionnaire contenant les comptes absolus des étiquettes de dépendance.
        dep_relative (dict): Un dictionnaire contenant les fréquences relatives des étiquettes de dépendance.

    Returns:
        dict: Le dictionnaire de données de sortie mis à jour avec les informations de dépendance.

    Cette fonction prend en entrée un dictionnaire de données de sortie, un dictionnaire de comptes absolus d'étiquettes de dépendance
    (`dep_absolue`) et un dictionnaire de fréquences relatives d'étiquettes de dépendance (`dep_relative`). Elle ajoute ces informations
    au dictionnaire de données de sortie en utilisant des traductions d'étiquettes de dépendance en français. Les étiquettes de dépendance
    sont ajoutées avec des préfixes 'Dep_absolue_' et 'Dep_relative_' correspondant à leur type, en français si une traduction existe,
    sinon en anglais. Le dictionnaire de données de sortie mis à jour est ensuite retourné.
    """
    
    # Traductions des étiquettes de dépendance en français
    dep_labels_fr = {
        'nsubj': 'Sujet_nominal',
        'ROOT': 'Racine',
        'det': 'Determinant',
        'amod': 'Modificateur_adjectival',
        'compound': 'Compose',
        'dobj': 'Objet_direct',
        'prep': 'Preposition',
        'pobj': 'Objet_de_preposition',
        'punct': 'Ponctuation',
        'expl': 'Element_expletif',
        'attr': 'Attribut',
        'acl': 'Clause_adjectivale',
        'advcl': 'Clause_adverbiale',
        'aux': 'Auxiliaire',
        'xcomp': 'Complement_ouvert',
        'conj': 'Conjonction',
        'cc': 'Conjonction_de_coordination',
        'neg': 'Negation',
        'dative': 'Datif'
    }

    # Ajouter les informations de dépendance absolue et relative au dictionnaire de données de sortie
    for dep, count in dep_absolue.items():
        output_data[f'Dep_absolue_{dep_labels_fr.get(dep, dep)}'] = count
    for dep, freq in dep_relative.items():
        output_data[f'Dep_relative_{dep_labels_fr.get(dep, dep)}'] = freq

    return output_data

def analyze_dependency_lengths(text, spacy_model):
    """
    Calcule la longueur moyenne et maximale des dépendances syntaxiques.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Tuple contenant la longueur moyenne et maximale des dépendances.
    """
    doc = spacy_model(text)
    lengths = []
    
    for token in doc:
        head = token.head
        distance = abs(token.i - head.i)  # Calcul de la distance entre les tokens
        lengths.append(distance)
    
    avg_length = sum(lengths) / len(lengths) if lengths else 0
    max_length = max(lengths) if lengths else 0

    return avg_length, max_length

def main_dependency_analysis(text, model):
    """
    Analyse les dépendances syntaxiques d'un texte dans une langue donnée.
    :param text: Texte à analyser.
    :param lang_code: Code de langue.
    :return: Dictionnaire avec les longueurs moyennes et maximales des dépendances.
    """

    avg_length, max_length = analyze_dependency_lengths(text, model)
    return {
        "Longueur_moyenne_des_dependances": avg_length,
        "Longueur_maximale_des_dependances": max_length
    }

def analyze_children(text, spacy_model):
    """
    Analyse le nombre d'enfants gauches et droits pour chaque mot.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Tuple contenant les sommes totales des enfants gauches et droits.
    """
    doc = spacy_model(text)
    left_children, right_children = 0, 0

    for token in doc:
        left_children += token.n_lefts
        right_children += token.n_rights

    total_tokens = len(text.split())

    avg_left_children = left_children / total_tokens if total_tokens else 0
    avg_right_children = right_children / total_tokens if total_tokens else 0
    
    return {
        "Moyenne_enfants_gauches": avg_left_children,
        "Moyenne_enfants_droits": avg_right_children,
        "Total_enfants_gauches": left_children,
        "Total_enfants_droits": right_children
    }

def verbe_inflection_relatif(nombre_verbe_inflexion, nombre_mots):
    """
    Calcule le nombre relatif de verbes à l'infinitif dans un texte.
    :param nombre_verbe_inflexion: Nombre de verbes conjugués.
    :param nombre_verbe: Nombre total de mots.
    :return: Nombre relatif de verbes conjugués par rapport au nombre de mots.
    """
    return nombre_verbe_inflexion / nombre_mots if nombre_mots else 0

def analyze_subordinate_clauses(text, spacy_model):
    """
    Analyse et compte les clauses subordonnées dans le texte.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Dictionnaire avec le comptage des types de clauses subordonnées.
    """
    doc = spacy_model(text)
    clause_counts = {
        "csubj": 0,  # Sujets clausaux
        "xcomp": 0,  # Compléments clausaux (sujet contrôlé)
        "ccomp": 0,  # Compléments clausaux (sujet non contrôlé)
        "advcl": 0,  # Modificateurs de clauses adverbiaux
        "acl": 0     # Modificateurs de clauses adnominaux
    }

    for token in doc:
        if token.dep_ in clause_counts:
            clause_counts[token.dep_] += 1
            
    total_tokens = len(text.split())

    # Calcul des fréquences relatives
    relative_frequencies = {dep: count / total_tokens for dep, count in clause_counts.items()}

    return {
        "Nombre_absolu": clause_counts,
        "Frequence_relative": relative_frequencies
    }

def translate_variables_subordinate_close_to_french(input_dict):
    """
    Traduit les clés du dictionnaire de l'anglais vers le français.
    :param input_dict: Dictionnaire avec des clés en anglais.
    :return: Nouveau dictionnaire avec des clés en français.
    """
    translation_dict = {
        'csubj': 'Sujets_Clausaux',
        'xcomp': 'Complements_Clausaux_Controles',
        'ccomp': 'Complements_Clausaux_Non_Controles',
        'advcl': 'Modificateurs_Clauses_Adverbiaux',
        'acl': 'Modificateurs_Clauses_Adnominaux'
    }

    # Traduire les clés du dictionnaire 'Nombre_absolu'
    new_absolute_counts = {translation_dict.get(k, k): v for k, v in input_dict['Nombre_absolu'].items()}

    # Traduire les clés du dictionnaire 'Frequence_relative'
    new_relative_freqs = {translation_dict.get(k, k): v for k, v in input_dict['Frequence_relative'].items()}

    return {
        'Nombre_absolu': new_absolute_counts,
        'Frequence_relative': new_relative_freqs
    }

def calculate_average_sentence_length(text, spacy_model):
    """
    Calcule la longueur moyenne des phrases dans le texte.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Longueur moyenne des phrases.
    """
    doc = spacy_model(text)
    sentences = list(doc.sents)
    total_words = sum(len(sentence) for sentence in sentences)
    average_length = total_words / len(sentences) if sentences else 0

    return average_length

def count_incomplete_sentences(text, spacy_model, total_words):
    """
    Compte les phrases incomplètes dans le texte.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Nombre total de phrases incomplètes.
    """
    doc = spacy_model(text)
    incomplete_sentences = 0

    for sentence in doc.sents:
        has_verb = has_subject = False
        for token in sentence:
            if token.pos_ == "VERB":
                has_verb = True
            if "subj" in token.dep_:
                has_subject = True
        if not (has_verb and has_subject):
            incomplete_sentences += 1

    return {
        "Nombre_absolu_phrases_incompletes": incomplete_sentences,
        "Frequence_relative_phrases_incompletes": incomplete_sentences / total_words if total_words else 0
    }

def count_prepositional_sentences(text, spacy_model, total_words):
    """
    Compte les phrases prépositionnelles dans le texte.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Nombre total de phrases prépositionnelles.
    """
    doc = spacy_model(text)
    prepositional_sentences = 0

    for sentence in doc.sents:
        for token in sentence:
            if token.pos_ == "ADP":  # ADP est la catégorie de préposition en spaCy
                if any(child.dep_ in ["pobj", "dobj"] for child in token.children):  # Objet de la préposition
                    prepositional_sentences += 1
                    break

    return {
        "Nombre_absolu_phrases_prepositionnelles": prepositional_sentences,
        "Frequence_relative_phrases_prepositionnelles": prepositional_sentences / total_words if total_words else 0
    }

def count_verbal_sentences(text, spacy_model, total_words):
    """
    Compte les phrases verbales dans le texte.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Nombre total de phrases verbales.
    """
    doc = spacy_model(text)
    verbal_sentences = 0

    for sentence in doc.sents:
        if any(token.pos_ == "VERB" for token in sentence):
            verbal_sentences += 1

    return {
        "Nombre_absolu_phrases_verbales": verbal_sentences,
        "Frequence_relative_phrases_verbales": verbal_sentences / total_words if total_words else 0
    }

def analyze_nominal_sentences(text, spacy_model, total_words):
    """
    Analyse et calcule le nombre et la longueur moyenne des phrases nominales.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Nombre total et longueur moyenne des phrases nominales.
    """
    doc = spacy_model(text)
    nominal_sentences = [chunk for chunk in doc.noun_chunks]
    total_nominal_sentences = len(nominal_sentences)
    total_length = sum(len(chunk) for chunk in nominal_sentences)
    average_length = total_length / total_nominal_sentences if total_nominal_sentences else 0
    
    return {
        "Nombre_absolu_phrases_nominales": total_nominal_sentences,
        "Longueur_moyenne_phrases_nominales": average_length,
        "Frequence_relative_phrases_nominales": total_nominal_sentences / total_words if total_words else 0
    }

def count_verb_tenses(text, spacy_model, total_words):
    """
    Compte les verbes conjugués au présent, au passé et au futur.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Dictionnaire avec le nombre de verbes pour chaque temps.
    """
    doc = spacy_model(text)
    tenses = {
        "present": 0,
        "past": 0,
        "future": 0
    }

    for token in doc:
        if token.pos_ == "VERB":
            if token.tag_ in ["VBP", "VBZ", "VBG"]:  # Tags typiques pour le présent en anglais
                tenses["present"] += 1
            elif token.tag_ in ["VBD", "VBN"]:  # Tags typiques pour le passé en anglais
                tenses["past"] += 1
            # Remarque: le futur en anglais est souvent marqué par des auxiliaires et n'a pas de tag spécifique.

    return {
        "Nombre_absolu": tenses,
        "Frequence_relative": {tense: count / total_words for tense, count in tenses.items()}
    }

def calculate_clauses_per_sentence(text, spacy_model):
    """
    Calcule le nombre moyen de clauses par phrase.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Nombre moyen de clauses par phrase.
    """
    doc = spacy_model(text)
    total_sentences = len(list(doc.sents))
    total_clauses = 0

    for sentence in doc.sents:
        clauses = [tok for tok in sentence if tok.dep_ in ["csubj", "ccomp", "xcomp"]]
        total_clauses += len(clauses)

    average_clauses = total_clauses / total_sentences if total_sentences else 0

    return average_clauses

def calculate_nouns_with_determiners_proportion(text, spacy_model):
    """
    Calcule la proportion de noms accompagnés de déterminants.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Proportion de noms avec déterminants.
    """
    doc = spacy_model(text)
    total_nouns = 0
    nouns_with_determiners = 0

    for token in doc:
        if token.pos_ == "NOUN":
            total_nouns += 1
            if any(child.dep_ == "det" for child in token.children):
                nouns_with_determiners += 1

    proportion = nouns_with_determiners / total_nouns if total_nouns else 0

    return proportion

def count_coordinated_sentences(text, spacy_model, lang_code, total_words):
    """
    Compte les phrases coordonnées dans le texte.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :param lang_code: Code de langue.
    :return: Nombre total de phrases coordonnées.
    """
    doc = spacy_model(text)
    coordinated_sentences = 0

    # Définition des conjonctions de coordination selon la langue
    if lang_code == 'English':
        coordination_conjunctions = {"and", "but", "for", "nor", "or", "yet", "so"}
    elif lang_code == 'Francais':
        coordination_conjunctions = {"et", "mais", "ou", "donc", "or", "ni", "car"}

    for sentence in doc.sents:
        if any(token.lower_ in coordination_conjunctions for token in sentence):
            coordinated_sentences += 1

    return {
        "Nombre_absolu_phrases_coordonnees": coordinated_sentences,
        "Frequence_relative_phrases_coordonnees": coordinated_sentences / total_words if total_words else 0
    }



