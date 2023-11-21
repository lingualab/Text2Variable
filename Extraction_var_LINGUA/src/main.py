from load_models import SpaCyModelLoader
import argparse
import os
import json
from Importation_JSON import read_json_file
from Save_JSON import save_json_file
from Mecanique_de_production_de_la_parole import compter_lemmes, compteur_fragments, compteur_fragment_anciennce_version
from Fluence import pauses_remplies, pauses_silencieuses, nombre_repetition_mot
from Caracteristiques_lexicales import Parts_of_Speech, count_open_closed_class_words, compter_verbes_conjugues, compter_gerondifs, calculer_ratios, count_light_verbs, indice_de_Brunet
import string
from Caracteristiques_pragmatiques import coherence_locale

def main():
    # Créez un analyseur d'arguments en ligne de commande
    parser = argparse.ArgumentParser(description="Rassemble les interventions et enregistre au format JSON.")

    # Ajoutez des arguments pour le fichier d'entrée, le nom du fichier de sortie et le dossier de sortie
    parser.add_argument("input_name", help="Nom du fichier JSON d'entrée")
    parser.add_argument("Taille_model_spacy", help="Taille du modèle spacy (sm, md, lg, trf)")
    parser.add_argument("-o", "--output_name", help="Nom du fichier JSON de sortie (optionnel)")
    parser.add_argument("-d", "--output_dir", help="Dossier de sortie (optionnel)")

    # Analysez les arguments de la ligne de commande
    args = parser.parse_args()

    # Vérifiez si le fichier d'entrée existe
    if not os.path.exists(args.input_name):
        print(f"Le fichier d'entrée {args.input_name} n'existe pas.")
        return

    # Lire le fichier JSON d'entrée
    texte_input = read_json_file(args.input_name)

    if texte_input is None:
        print("Impossible de lire le fichier d'entrée.")
        return

    # Variables :
    langue = texte_input.get("Langue", "N/A")
    ID = texte_input.get("ID", "N/A")
    texte_brut = texte_input.get("Texte_original", "N/A")
    texte_nettoye = texte_input.get("Texte_nettoye", "N/A")
    texte_tokenise = texte_input.get("Texte_tokenizes", "N/A")
    texte_tokenise_sans_stop = texte_input.get("Texte_tokenizes_sans_stop", "N/A")
    texte_lemmatise = texte_input.get("Lemmes", "N/A")
    
    # Déterminer le nom du fichier de sortie
    if args.output_name is None:
        # Utilise le nom du participant s'il est disponible
        participant_id = ID
        if participant_id != "N/A":
            output_name = f"{participant_id}.json"
        else:
            print("Le nom du participant est introuvable. Spécifiez un nom de fichier de sortie.")
            return
    else:
        # Utilisez le nom spécifié en ligne de commande avec l'extension .json
        output_name = args.output_name + ".json"

    # Déterminer le dossier de sortie
    if args.output_dir is not None:
        output_dir = args.output_dir
    else:
        output_dir = "Results"  # Dossier de sortie par défaut

    # Charger le modèle SpaCy  
    ### Petit modele pour les tests (plus rapide)
    loader = SpaCyModelLoader()
    model, nom_du_modele = loader.load(langue, args.Taille_model_spacy) # "Francais" ou "English" et "sm", "md", "lg", "trf"

    ######## Mecanique de production de la parole ########
    
    # Compter le nombre de lemmes dans le texte nettoyé
    nombre_de_lemmes = compter_lemmes(texte_lemmatise)
    texte_token_without_punctuation = [token for token in texte_tokenise if token not in string.punctuation]
    nombre_de_fragments = compteur_fragments(texte_token_without_punctuation, langue) # print_fragments=False
    nombre_de_fragments_autre_methode = compteur_fragment_anciennce_version(texte_tokenise, langue)

    print("Coompteur de fragments en contexte non fonctionnel pour le moment")

    ######## Mecanique de production de la parole ########
    
    # Compter le nombre de pauses silencieuses dans le texte brut
    nombre_pauses_silencieuses = pauses_silencieuses(texte_brut, langue)
    # Compter le nombre de pauses remplies dans le texte brut
    nombre_pauses_remplies = pauses_remplies(texte_brut, langue)
    # Compter le nombre de répétitions de mots dans le texte lemmatize
    nombre_lemmes_differents, nombre_repetitions = nombre_repetition_mot(texte_lemmatise)

    ######## Caractéristiques lexicales ########
    
    # Parts-of-Speech*
    POS_Dict = Parts_of_Speech(texte_brut, model)
    # Compter les mots de classe ouverte et fermée
    mot_ouvert, mot_ferme = count_open_closed_class_words(texte_brut, model)
    # Compter les verbes avec inflexions
    nombre_verbe_inflexion = compter_verbes_conjugues(texte_brut, langue, model)
    # Compter les gerondifs
    nombre_gerondif = compter_gerondifs(texte_brut, langue, model)
    # Extraire les valeurs "count" pour Verbe, Nom et Pronom
    total_verbes = POS_Dict.get("Verbe", {}).get("count", "N/A")
    total_noms = POS_Dict.get("Nom", {}).get("count", "N/A")
    total_pronoms = POS_Dict.get("Pronom", {}).get("count", "N/A")
    total_des_mots = len(texte_nettoye)
    # Ratio de différentes Parts-of-Speech et types de mots
    ratios = calculer_ratios(total_verbes, total_noms, total_pronoms, nombre_verbe_inflexion, mot_ouvert, mot_ferme, nombre_gerondif, total_des_mots)
    
    # Compteur de verbes légers
    print("Compteur de verbes légers non fonctionnel pour le moment")
    
    # Pronoms déictiques*
    
    # Termes indéfinis*
    
    # Moving Average Type- Token Ratio (MATTR)

    # Statistique R de Honoré
    
    # Indice W de Brunet
    brunet_w_indice = indice_de_Brunet(total_des_mots, nombre_lemmes_differents)
    
    # Familiarité 
    
    # Imageabilité
    
    # Concrétude

    # Fréquence des mots dans le langage courant
    
    # Valence 

    ######## Caractéristiques semantiques ########
    
    # 25 informations de contenu (ICUs)
    
    # Nombre total d’ICUs
    
    # Efficacité
    
    # Densité d’idées
    
    ######## Caractéristiques syntaxiques ########
    
    # Dépendances syntaxiques universelles*
    
    # Longueur des dépendances syntaxiques
    
    # Enfants gauches et droits*

    # Verbes avec inflexions*
    # Déla1 réalisé dans les catgeories lexicales
    
    # Clauses subordonnées*
    
    # Longueur moyenne des phrases
    
    # Phrases incomplètes*
    
    # Nombre de phrases prépositionnelles* (Boschi et al., 2017)
    
    # Nombre de phrases verbales*
    
    # Longueur et nombre de phrases nominales*
    
    # Temps de verbes utilisés*
    
    # Clauses par phrase
    
    # Proportion de noms accompagnés de déterminants
    
    # Phrases coordonnées* (Boschi et al., 2017)
    
    ######## Caractéristiques pragmatiques ########
    
    # Cohérence locale
    #coherence_locale_ = coherence_locale(texte_brut, model)
    #print("Coherence locale : ", coherence_locale_)
    # Mots dénotant l’incertitude*
    
    # Difficultés à trouver les bons mots*
    
    # Connotation du discours
    
    # Expressions formulaiques* (Van Lancker Sidtis et al., 2015)
    
    # Modalisations* (Boschi et al., 2017, Boyé et al., 2014)
    
    # Mots de remplissage*
    
    
    
    
    
    # Ajouter les informations au dictionnaire de sortie
    output_data = {
        "ID": participant_id,
        "Langue": texte_input.get("Langue", "N/A"),
        "SpaCy_Model" : nom_du_modele,
        "Nombre_de_lemmes": nombre_de_lemmes,
        "Nombre_de_fragments": nombre_de_fragments,
        "Nombre_de_fragments_autre_methode": nombre_de_fragments_autre_methode,
        "Nombre_de_pauses_silencieuses": nombre_pauses_silencieuses,
        "Nombre_de_pauses_remplies": nombre_pauses_remplies,
        "Nombre_de_lemmes_differents": nombre_lemmes_differents,
        "Nombre_de_repetitions_mots": nombre_repetitions,
        'Adjectif' : POS_Dict.get("Adjectif", "N/A"),
        'Preposition' : POS_Dict.get("Preposition", "N/A"),
        'Adverbe' : POS_Dict.get("Adverbe", "N/A"),
        'Auxiliaire' : POS_Dict.get("Auxiliaire", "N/A"),
        'Conjonction' : POS_Dict.get("Conjonction", "N/A"),
        'Conjonction_de_coordination' : POS_Dict.get("Conjonction_de_coordination", "N/A"),
        'Determinant' : POS_Dict.get("Determinant", "N/A"),
        'Interjection' : POS_Dict.get("Interjection", "N/A"),
        'Nom' : POS_Dict.get("Nom", "N/A"),
        'Numeral' : POS_Dict.get("Numeral", "N/A"),
        'Particule' : POS_Dict.get("Particule", "N/A"),
        'Pronom' : POS_Dict.get("Pronom", "N/A"),
        'Nom propre' : POS_Dict.get("Nom propre", "N/A"),
        'Ponctuation' : POS_Dict.get("Ponctuation", "N/A"),
        'Conjonction_de_subordination' : POS_Dict.get("Conjonction_de_subordination", "N/A"),
        'Symbole' : POS_Dict.get("Symbole", "N/A"),
        'Verbe' : POS_Dict.get("Verbe", "N/A"),
        'Autre' : POS_Dict.get("Autre", "N/A"),
        'Mots_de_classe_ouverte' : mot_ouvert,
        'Mots_de_classe_fermee' : mot_ferme,
        'Nombre_de_verbes_inflexion' : nombre_verbe_inflexion,
        'Nombre_de_gerondifs' : nombre_gerondif,
        'Pronoms/(Noms+Pronoms)' : ratios.get('Pronoms/(Noms+Pronoms)', "N/A"),
        'Noms/(Noms+Pronoms)' : ratios.get('Noms/(Noms+Pronoms)', "N/A"),
        'Noms/(Noms+Verbes)' : ratios.get('Noms/(Noms+Verbes)', "N/A"),
        'Verbes/(Noms+Verbes)' : ratios.get('Verbes/(Noms+Verbes)', "N/A"),
        'Verbes_avec_inflexions/Total_Verbes' : ratios.get('Verbes_avec_inflexions/Total_Verbes', "N/A"),
        'Mots_de_classe_ouverte/Total_Mots' : ratios.get('Mots_de_classe_ouverte/Total_Mots', "N/A"),
        'Mots_de_classe_fermee/Total_Mots' : ratios.get('Mots_de_classe_fermee/Total_Mots', "N/A"),
        'Gerondifs/Total_Verbes' : ratios.get('Gerondifs/Total_Verbes', "N/A"),
        'Gerondifs/Total_Mots' : ratios.get('Gerondifs/Total_Mots', "N/A"),
        'Brunet_W_indice' : brunet_w_indice
        
    }
    
    # Composez le chemin complet du fichier de sortie
    output_path = os.path.join(output_dir, output_name)
    
    # Enregistrez le fichier JSON de sortie
    # Convertir le dictionnaire en format JSON avec une indentation pour chaque élément
    output_json = json.dumps(output_data, indent=4)

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path + "_Data_Var.json", "w") as json_file:
        json_file.write(output_json)
    
    print(f"Le fichier {output_name} a été enregistré dans le dossier {output_dir}. L'extraction des diverses variables est finie.")


if __name__ == "__main__":
    main()