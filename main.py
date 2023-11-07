from src import Import_JSON
from src import basic_statistics
from src import coherence_style
from src import content_analysis
from src.lexical_analysis import LinguisticProcessor
from src.pauses_repetitions import PauseCounter
from src import statistical_analysis
from src import syntax_analysis
from src.load_models import SpaCyModelLoader
from src.lemmatization import TranscriptProcessor
from src.cleaner_transcription import TranscriptionCleaner
from src.Traitement_texte import TraitementDuTexte
from src.statistical_analysis import AnalyseTextuelle
from src.AnalyseFragmentaire import AnalyseFragmentaire
from src.pos_syntax_proportions import ProportionalAnalyser
from src.analyseurs_lexicaux import AnalyseurLemmesUniques, StatsHonoreBrunet, AnalyseurMATTR
import pandas as pd
import numpy as np

file_input = 'Documents/BCG14703.json'
name_input = 'BCG14703'
# Utilisation de la fonction lire_fichier_json pour charger les données
donnees = Import_JSON.read_json_file('Documents/BCG14703.json')
langue = donnees['participant']['Langue']
ID = donnees["participant"]["ID"]
Genre = donnees['participant']["Gender"]
Orientation_sexuelle = donnees['participant']["Sexual_orientation"] 
Performance_numerique = donnees['participant']["Digital_performance"]
Pays = donnees['participant']["Country"]
Sexe = donnees['participant']["Sex"]
Age = donnees['participant']["Age"]

# Extraction du contenu total des interventions dans test
interventions = [entry["contenu"] for entry in donnees["test"]["interventions"]]

# Chargement des différents modèles
### Petit modele pour les tests (plus rapide)
loader = SpaCyModelLoader()
alias, model = loader.load(langue, "sm") # "Francais" ou "English" et "sm", "md", "lg", "trf"

processor = TranscriptProcessor(alias)
# Appel de la méthode process_transcripts avec l'ID du participant et les interventions
processor.process_transcripts(donnees["participant"]["ID"], interventions)

# Si vous voulez sauvegarder les résultats dans un fichier
file_content, tagged_corpus = processor.write_to_file(name_input)

processor = LinguisticProcessor(tagged_corpus)
processed_data = processor.process_data()

counter = PauseCounter(interventions, langue)
pause_counts = counter.count_pauses()
# Initialisation des compteurs
total_empty_pauses = 0
total_filled_pauses = 0

# Parcourir la liste des résultats de PauseCounter
for pause_count in pause_counts:
    # Accumuler les comptes de pauses vides et remplies
    total_empty_pauses += pause_count['empty']
    total_filled_pauses += pause_count['filled']

# Créez une instance de la nouvelle classe avec vos données
transcript_processor = TranscriptionCleaner(interventions)
# Nettoyage
clean_transcription = transcript_processor.apply_cleaning_functions()

Comp_frag = basic_statistics.CompteurDeFragments(langue, clean_transcription)
fragments_count, total_fragments = Comp_frag.compter()

TraitementTexte = TraitementDuTexte(clean_transcription, alias)
Texte_traité = TraitementTexte.traiter()
Texte_traité_lié = " ".join(Texte_traité)

analyse = AnalyseTextuelle(Texte_traité_lié)
resultats = analyse.analyser()

# Créer un dictionnaire avec des clés pour chaque intervention
data = {
    "ID": ID,
    "Langue": langue,
    "Gender": Genre,
    "Sexual_orientation": Orientation_sexuelle,
    "Digital_performance": Performance_numerique,
    "Country": Pays,
    "Sex": Sexe,
    "Age": Age,
    "SpaCy_Model" : model,
    "Total_Empty_Pauses": total_empty_pauses,
    "Total_Filled_Pauses": total_filled_pauses,
    "Total_Fragments": total_fragments,
    "Longueur_moyenne_mots": resultats['longueur_moyenne_mots'],
    "Nombre_types_mots": resultats['nombre_types'],
    "Nombre_tokens_mots": resultats['nombre_tokens'],
}

data["Texte_traité"] = Texte_traité

for column in processed_data.columns:
    data[column] = processed_data[column].iloc[0]  # On suppose qu'il y a une seule ligne dans processed_data

analyseur = AnalyseFragmentaire(data, langue)
data = analyseur.traiter()

# Créez une instance de la nouvelle classe avec vos données
analyseur_proportionnel = ProportionalAnalyser(data)
data = analyseur_proportionnel.traiter()



# Supposons que vous avez un DataFrame nommé `donnees`
analyseur_lemmas = AnalyseurLemmesUniques(data)
analyseur_stats = StatsHonoreBrunet(data)
analyseur_mattr = AnalyseurMATTR(data)

# Utilisation des méthodes fournies par les classes selon les besoins
analyseur_lemmas.calculer_lemmas_uniques()
print(data["Nombre_tokens_mots"])
print(data["uniqueLemmas"])
print(data["Nombre_types_mots"])

#analyseur_stats.calculer_Honore_et_Brunet()
#analyseur_mattr.calculer_MATTR()

'''print(data.keys())
print(type(data))'''
# Créez un DataFrame en utilisant le dictionnaire, cela crée une ligne avec chaque intervention comme colonne
df = pd.DataFrame([data])

# Pour enregistrer le DataFrame dans un fichier CSV
df.to_csv('Results/your_dataframe.csv', index=False)