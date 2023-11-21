import numpy as np
import spacy

def cosine_similarity(a, b):
    """ Fonction a faire"""
    # Calcul de la similarité cosinus entre deux vecteurs
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def coherence_locale(text, nlp):
    " Fonction a faire"
    # Segmentation du texte en phrases
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    # Encodage des phrases
    embeddings = nlp.encode(sentences)

    # Calcul de la similarité cosinus entre chaque paire consécutive
    cosine_scores = [cosine_similarity(embeddings[i], embeddings[i+1]) for i in range(len(embeddings)-1)]

    # Moyenne des scores de similarité
    moyenne = sum(cosine_scores) / len(cosine_scores)
    # Retourne la moyenne des scores de similarité
    return moyenne

