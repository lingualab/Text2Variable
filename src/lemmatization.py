import spacy
import string
import os

class TranscriptProcessor:
    def __init__(self, lang_model=None, output_filename='checkingTags.txt'):
        # Si aucun modèle n'est fourni, nous chargerons le modèle anglais par défaut
        if lang_model is None:
            lang_model = spacy.load("en_core_web_sm")
            
        self.lang_model = lang_model
        self.tagged_corpus = {}
        self.output_filename = output_filename
        self.punctuation = set(string.punctuation) | {" ", "  "}

    def process_transcripts(self, participant_id, interventions):
        transcription = " ".join(interventions)

        # Appliquer spaCy sur la transcription
        depSample = self.lang_model(transcription)

        # Initialiser une liste pour stocker les informations de chaque token
        tokenList = []

        # Traitement des tokens
        for token in depSample:
            tokenTuple = (token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.n_lefts, 
                          token.n_rights, token.is_oov, token.has_vector, token.vector_norm)
            if tokenTuple[0] not in self.punctuation:
                tokenList.append(tokenTuple)

        # Stocker les informations du participant dans le dictionnaire
        self.tagged_corpus[participant_id] = tokenList

        for token in depSample:
            tokenTuple = (
                token.text, token.lemma_, token.pos_, token.tag_,
                token.dep_, token.n_lefts, token.n_rights,
                token.is_oov, token.has_vector, token.vector_norm
            )
            assert len(tokenTuple) == 10, "Le tuple de token n'a pas la bonne taille."
            if tokenTuple[0] not in self.punctuation:
                tokenList.append(tokenTuple)
        
        print("Les fichiers texte ont été tokenisés avec succès.")


    def write_to_file(self, output_file_name=None):
        if output_file_name is None:
            output_file_name = self.output_filename

        # Préfixer le chemin du dossier "Documents" au nom du fichier
        path_to_save = os.path.join("Results", output_file_name + ".txt")

        file_content = ""
        for participant, tokens in self.tagged_corpus.items():
            file_content += "{}\n".format(participant)
            for word in tokens:
                file_content += ",".join(map(str, word)) + "\n"

        with open(path_to_save, 'w') as file:
            file.write(file_content)

        print(f"Les données ont été enregistrées avec succès dans le fichier '{path_to_save}'.")
        
        return file_content, self.tagged_corpus



