from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")
model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

from .Database_linguistique import uncertainty_words, formulaic_expressions, expressions, filler_expressions_dict

def calculate_cosine_similarity_between_sentences(text, spacy_model):
    """
    Calcule la similarité cosinus moyenne entre les phrases d'un texte.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :return: Score moyen de similarité cosinus.
    """
    doc = spacy_model(text)
    sentences = list(doc.sents)
    sentence_vectors = [sentence.vector for sentence in sentences]
    total_similarity = 0
    comparisons = 0

    for i in range(len(sentence_vectors) - 1):
        similarity = cosine_similarity([sentence_vectors[i]], [sentence_vectors[i + 1]])[0][0]
        total_similarity += similarity
        comparisons += 1

    average_similarity = total_similarity / comparisons if comparisons else 0

    return float(average_similarity)

def count_uncertainty_words(text, spacy_model, langue_code, total_words):
    """
    Compte les occurrences de mots dénotant l'incertitude.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :param lang_code: Code de langue.
    :return: Nombre total d'occurrences de ces mots.
    """

    # Vérifie si la langue est prise en charge
    if langue_code not in uncertainty_words:
        raise ValueError(f"La langue '{langue_code}' n'est pas prise en charge")
    
    doc = spacy_model(text)
    count = sum(token.text.lower() in uncertainty_words[langue_code] for token in doc)

    return {
        "Nombre_absolu_mots_incertitude": count,
        "Frequence_relative_mots_incertitude": count / total_words if total_words else 0
    }

def count_lexical_access_difficulty_words(text, spacy_model, lang_code, total_words):
    """
    Compte les instances de mots indiquant des difficultés d'accès lexical.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :param lang_code: Code de langue.
    :param total_words: Nombre total de mots dans l'échantillon.
    :return: Dictionnaire avec le nombre absolu et relatif de ces mots.
    """
    # Mots indiquant des difficultés d'accès lexical en anglais et en français
    difficulty_words = {
        'English': {"know", "remember", "unable"},
        'Francais': {"savoir", "se souvenir", "incapable"}  
    }
    
    # Vérifie si la langue est prise en charge
    if lang_code not in difficulty_words:
        raise ValueError(f"La langue '{lang_code}' n'est pas prise en charge")
    
    doc = spacy_model(text)
    count = sum(token.text.lower() in difficulty_words[lang_code] for token in doc)

    return {
        "Nombre_absolu": count,
        "Frequence_relative": count / total_words if total_words else 0
    }

def count_formulaic_expressions(text, lang_code, total_words):
    """
    Compte les occurrences d'expressions formulaiques dans le texte.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :param lang_code: Code de langue.
    :param total_words: Nombre total de mots dans l'échantillon.
    :return: Dictionnaire avec le nombre absolu et relatif de ces expressions.
    """
    # Vérifie si la langue est prise en charge
    if lang_code not in formulaic_expressions:
        raise ValueError(f"La langue '{lang_code}' n'est pas prise en charge")
    
    count = sum(text.count(expression) for expression in formulaic_expressions[lang_code])

    return {
        "Nombre_absolu": count,
        "Frequence_relative": count / total_words if total_words else 0
    }

def analyze_modal_expressions(text, spacy_model, lang_code):
    """
    Analyse et compte les expressions de modalisation dans le texte. 
    Opinions d’un individu concernant le contenu de sa description 
    (ou ce qui se passe sur l’image à décrire) incluant les doutes et les inquiétudes par rapport à sa production.
    
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :param lang_code: Code de langue ('English' pour anglais, 'Francais' pour français).
    :return: Dictionnaire avec le nombre absolu et relatif des expressions de modalisation.
    """

    doc = spacy_model(text)
    total_words = len([token for token in doc if not token.is_punct and not token.is_space])
    count = sum(doc.text.count(expression) for expression in expressions[lang_code])
    relative_frequency = count / total_words if total_words else 0

    return {
        "Nombre_absolu": count,
        "Frequence_relative": relative_frequency
    }

def analyze_filler_words(text, spacy_model, total_words, lang_code):
    """
    Analyse et compte les mots de remplissage dans le texte en fonction de la langue.
    :param text: Texte à analyser.
    :param spacy_model: Modèle spaCy chargé.
    :param total_words: Nombre total de mots dans le texte.
    :param lang_code: Code de langue ('English' pour l'anglais, 'Francais' pour le français).
    :return: Dictionnaire avec le nombre absolu et relatif des mots de remplissage.
    """
    # Vérification de la prise en charge de la langue
    if lang_code not in filler_expressions_dict:
        return {"Erreur": "Langue non prise en charge"}

    filler_expressions = filler_expressions_dict[lang_code]

    # Utilisation de spaCy pour une tokenisation plus précise
    doc = spacy_model(text)
    
    # Comptage des expressions de remplissage
    count = sum(doc.text.count(expression) for expression in filler_expressions)
    
    # Calcul de la fréquence relative
    relative_frequency = count / total_words if total_words else 0

    return {
        "Nombre_absolu": count,
        "Frequence_relative": relative_frequency
    }

def get_emotion(text):
    input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')
    output = model.generate(input_ids=input_ids, max_length=2)
    dec = [tokenizer.decode(ids) for ids in output]
    label = dec[0]
    # Supprimer le token <pad> de la sortie
    label = label.replace("<pad>", "").strip()
    return label

def get_sentiment(text):
    """
    Analyse le sentiment d'un texte utilisant le modèle mrm8488/t5-base-finetuned-emotion
    :param text: Texte à analyser.
    :return: Étiquette de sentiment.
    """
    # Création de la pipeline de sentiment analysis
    sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
    # Analyse du sentiment
    result = sentiment_task(text)
    # Récupération de l'étiquette de sentiment
    label = result[0]['label']
    return label
