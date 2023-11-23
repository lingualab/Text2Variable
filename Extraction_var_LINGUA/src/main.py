from load_models import SpaCyModelLoader
import argparse
import numpy as np
import os
import json
import string
from Importation_JSON import read_json_file
from Save_JSON import save_json_file
# Importation des fonctions permettant l'extraction des variables decrivant la mecanique de production de la parole
from Mecanique_de_production_de_la_parole import compter_lemmes, compteur_fragments, compteur_fragment_anciennce_version
# Importation des fonctions permettant l'extraction des variables decrivant la fluence
from Fluence import pauses_remplies, pauses_silencieuses, nombre_repetition_mot
# Importation des fonctions permettant l'extraction des caractéristiques lexicales
from Caracteristiques_lexicales import (
    Parts_of_Speech,
    count_open_closed_class_words,
    compter_verbes_conjugues,
    compter_gerondifs,
    calculer_ratios,
    count_light_verbs,
    indice_de_Brunet,
    count_deictic_pronouns,
    ratio_termes_indefinis,
    calculer_mattr,
    calculer_nbres_mots_unique,
    stat_R_Honore
    
)

from Caracteristiques_semantiques import (
    analyse_text,
    nombre_ICU,
    calculer_ratio_mots_par_ICU_VRAI,
    densite_idees
)

from Caracteristiques_syntaxiques import (
    analyze_text_dependencies,
    add_dependency_info,
    main_dependency_analysis,
    analyze_children,
    verbe_inflection_relatif,
    analyze_subordinate_clauses,
    translate_variables_subordinate_close_to_french,
    calculate_average_sentence_length,
    count_incomplete_sentences,
    count_prepositional_sentences,
    count_verbal_sentences,
    analyze_nominal_sentences,
    count_verb_tenses,
    calculate_clauses_per_sentence,
    calculate_nouns_with_determiners_proportion,
    count_coordinated_sentences
    
)
# Importation des fonctions permettant l'extraction des caractéristiques pragmatiques
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

    print("Compteur de fragments en contexte non fonctionnel pour le moment")

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
    nombre_de_pronoms_deictiques = count_deictic_pronouns(texte_brut, langue, model)
    # Termes indéfinis*
    ratio_nbre_termes_indefinis, nbre_termes_indefinis = ratio_termes_indefinis(texte_brut, langue, model)
    # Moving Average Type- Token Ratio (MATTR)
    MATTR_10 = calculer_mattr(texte_brut, 10, model)
    MATTR_25 = calculer_mattr(texte_brut, 25, model)
    MATTR_40 = calculer_mattr(texte_brut, 40, model)
    # Statistique R de Honoré
    nbres_mots_unique = calculer_nbres_mots_unique(texte_nettoye)  # Le nombre de mots uniques dans le texte
    stat_honore = stat_R_Honore(total_des_mots, nombre_lemmes_differents, nbres_mots_unique)
    # Indice W de Brunet
    brunet_w_indice = indice_de_Brunet(total_des_mots, nombre_lemmes_differents)
    
    # Familiarité 
    print("Familiarité non fonctionnel pour le moment")
    # Imageabilité
    print("Imageabilité non fonctionnel pour le moment")
    # Concrétude
    print("Concrétude non fonctionnel pour le moment")
    # Fréquence des mots dans le langage courant
    print("Fréquence des mots dans le langage courant non fonctionnel pour le moment")
    # Valence 
    print("Valence non fonctionnel pour le moment")
    
    ######## Caractéristiques semantiques ########
    
    # 25 informations de contenu (ICUs)
    dict_info_contenu_T_or_F = analyse_text(texte_brut, langue)  # Analyse du texte en anglais
    # Nombre total d’ICUs
    nombre_de_ICU_TRUE = nombre_ICU(dict_info_contenu_T_or_F)
    # Efficacité
    efficacite_ICU = calculer_ratio_mots_par_ICU_VRAI(total_des_mots, nombre_de_ICU_TRUE)
    # Densité d’idées
    densite_idees__ = densite_idees(texte_brut, model, tailles_fenetres=[3, 10, 25, 40])
    
    
    ######## Caractéristiques syntaxiques ########
    
    # Dépendances syntaxiques universelles*
    dependance_absolu, dependance_relative = analyze_text_dependencies(texte_brut, model)
    # Longueur des dépendances syntaxiques
    len_dep_syntaxique = main_dependency_analysis(texte_brut, model)
    # Enfants gauches et droits*
    enfants_droite_gauche = analyze_children(texte_brut, model)
    # Verbes avec inflexions 
    verbe_inflexion_relatif = verbe_inflection_relatif(nombre_verbe_inflexion, total_des_mots)
    # Clauses subordonnées*
    dict_clauses_subordonnees = analyze_subordinate_clauses(texte_brut, model)
    dict_traduit_clauses_subordonnees = translate_variables_subordinate_close_to_french(dict_clauses_subordonnees)
    # Longueur moyenne des phrases
    longueur_moyenne_phrases = calculate_average_sentence_length(texte_brut, model)
    # Phrases incomplètes*    
    nbre_phrases_incompletes = count_incomplete_sentences(texte_brut, model, total_des_mots)
    # Nombre de phrases prépositionnelles* (Boschi et al., 2017)
    nbre_phrases_prepositionnelles = count_prepositional_sentences(texte_brut, model, total_des_mots)
    # Nombre de phrases verbales*
    nbre_phrases_verbales = count_verbal_sentences(texte_brut, model, total_des_mots)
    # Longueur et nombre de phrases nominales*
    phrases_nominales =  analyze_nominal_sentences(texte_brut, model, total_des_mots)
    # Temps de verbes utilisés*
    temps_verbes = count_verb_tenses(texte_brut, model, total_des_mots)
    # Clauses par phrase
    nbre_clauses_par_phrase = calculate_clauses_per_sentence(texte_brut, model)
    # Proportion de noms accompagnés de déterminants
    proportion_noms_determinants = calculate_nouns_with_determiners_proportion(texte_brut, model)
    # Phrases coordonnées* (Boschi et al., 2017)
    coordonnees_phrases = count_coordinated_sentences(texte_brut, model, langue, total_des_mots)
    print("Phrases coordonnees : ", coordonnees_phrases)
    
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
        "Nombre_de_mots": total_des_mots,
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
        'Nombre_de_pronoms_deictiques' : nombre_de_pronoms_deictiques.get("total_deictic_pronouns", "N/A"),
        'Nombre_de_pronoms_deictiques_spatiaux' : nombre_de_pronoms_deictiques.get("spatial", "N/A"),
        'Nombre_de_pronoms_deictiques_personnels' : nombre_de_pronoms_deictiques.get("personal", "N/A"),
        'Nombre_de_pronoms_deictiques_temporels' : nombre_de_pronoms_deictiques.get("temporal", "N/A"),
        'Nombre_de_termes_indefinis' : nbre_termes_indefinis,
        'Ratio_termes_indefinis' : ratio_nbre_termes_indefinis,
        'MATTR_10' : MATTR_10,
        'MATTR_25' : MATTR_25,
        'MATTR_40' : MATTR_40,
        'Nombre_de_mots_uniques' : nbres_mots_unique,
        'Statistique_R_de_Honore' : stat_honore,
        'Brunet_W_indice' : brunet_w_indice,
        'Nombre_ICU_TRUE' : nombre_de_ICU_TRUE,
        'Efficacite_ICU' : efficacite_ICU,
        'Longueur_moyenne_des_dependances' : len_dep_syntaxique.get("Longueur_moyenne_des_dependances", "N/A"),
        'Longueur_maximale_des_dependances' : len_dep_syntaxique.get("Longueur_maximale_des_dependances", "N/A"),
        'Moyenne_enfants_gauches' : enfants_droite_gauche.get("Moyenne_enfants_gauches", "N/A"),
        'Moyenne_enfants_droits' : enfants_droite_gauche.get("Moyenne_enfants_droits", "N/A"),
        'Total_enfants_gauches' : enfants_droite_gauche.get("Total_enfants_gauches", "N/A"),
        'Total_enfants_droits' : enfants_droite_gauche.get("Total_enfants_droits", "N/A"),
        'Nombre_de_verbes_inflexion' : nombre_verbe_inflexion,
        'Verbe_inflection_relatif' : verbe_inflexion_relatif,
        'Sujets_Clausaux_absolu' : dict_traduit_clauses_subordonnees.get("Nombre_absolu", {}).get("Sujets_Clausaux", "N/A"),
        'Sujets_Clausaux_relatif' : dict_traduit_clauses_subordonnees.get("Frequence_relative", {}).get("Sujets_Clausaux", "N/A"),
        'Complements_Clausaux_Controles_absolu' : dict_traduit_clauses_subordonnees.get("Nombre_absolu", {}).get("Complements_Clausaux_Controles", "N/A"),
        'Complements_Clausaux_Controles_relatif' : dict_traduit_clauses_subordonnees.get("Frequence_relative", {}).get("Complements_Clausaux_Controles", "N/A"),
        'Complements_Clausaux_Non_Controles_absolu' : dict_traduit_clauses_subordonnees.get("Nombre_absolu", {}).get("Complements_Clausaux_Non_Controles", "N/A"),
        'Complements_Clausaux_Non_Controles_relatif' : dict_traduit_clauses_subordonnees.get("Frequence_relative", {}).get("Complements_Clausaux_Non_Controles", "N/A"),
        'Modificateurs_Clauses_Adverbiaux_absolu' : dict_traduit_clauses_subordonnees.get("Nombre_absolu", {}).get("Modificateurs_Clauses_Adverbiaux", "N/A"),
        'Modificateurs_Clauses_Adverbiaux_relatif' : dict_traduit_clauses_subordonnees.get("Frequence_relative", {}).get("Modificateurs_Clauses_Adverbiaux", "N/A"),
        'Modificateurs_Clauses_Adnominaux_absolu' : dict_traduit_clauses_subordonnees.get("Nombre_absolu", {}).get("Modificateurs_Clauses_Adnominaux", "N/A"),
        'Modificateurs_Clauses_Adnominaux_relatif' : dict_traduit_clauses_subordonnees.get("Frequence_relative", {}).get("Modificateurs_Clauses_Adnominaux", "N/A"),
        'Longueur_moyenne_phrases' : longueur_moyenne_phrases,
        'Nombre_de_phrases_incompletes_absolu' : nbre_phrases_incompletes.get("Nombre_absolu_phrases_incompletes", "N/A"),
        'Nombre_de_phrases_incompletes_relatif' : nbre_phrases_incompletes.get("Frequence_relative_phrases_incompletes", "N/A"),
        'Nombre_de_phrases_prepositionnelles_absolu' : nbre_phrases_prepositionnelles.get("Nombre_absolu_phrases_prepositionnelles", "N/A"),
        'Nombre_de_phrases_prepositionnelles_relatif' : nbre_phrases_prepositionnelles.get("Frequence_relative_phrases_prepositionnelles", "N/A"),        
        'Nombre_de_phrases_verbales_absolu' : nbre_phrases_verbales.get("Nombre_absolu_phrases_verbales", "N/A"),
        'Nombre_de_phrases_verbales_relatif' : nbre_phrases_verbales.get("Frequence_relative_phrases_verbales", "N/A"),
        'Nombre_absolu_phrases_nominales' : phrases_nominales.get("Nombre_absolu_phrases_nominales", "N/A"),
        'Longueur_moyenne_phrases_nominales' : phrases_nominales.get("Longueur_moyenne_phrases_nominales", "N/A"),
        'Frequence_relative_phrases_nominales' : phrases_nominales.get("Frequence_relative_phrases_nominales", "N/A"),
        'Nbre_verb_present_absolu' : temps_verbes.get("Nombre_absolu", {}).get("present", "N/A"),
        'Nbre_verb_present_relatif' : temps_verbes.get("Frequence_relative", {}).get("present", "N/A"),
        'Nbre_verb_past_absolu' : temps_verbes.get("Nombre_absolu", {}).get("past", "N/A"),
        'Nbre_verb_past_relatif' : temps_verbes.get("Frequence_relative", {}).get("past", "N/A"),
        'Nbre_verb_future_absolu' : temps_verbes.get("Nombre_absolu", {}).get("future", "N/A"),
        'Nbre_verb_future_relatif' : temps_verbes.get("Frequence_relative", {}).get("future", "N/A"),
        "Nbre_clauses_par_phrase" : nbre_clauses_par_phrase,
        "Proportion_noms_determinants" : proportion_noms_determinants,
        "Nombre_de_phrases_coordonnees" : coordonnees_phrases.get("Nombre_absolu_phrases_coordonnees", "N/A"),
        "Frequence_relative_phrases_coordonnees" : coordonnees_phrases.get("Frequence_relative_phrases_coordonnees", "N/A")
        
        
    }

    # Convertir les valeurs float32 en float
    for cle in densite_idees__:
        if isinstance(densite_idees__[cle], np.float32):
            densite_idees__[cle] = float(densite_idees__[cle])
            
    for cle, valeur in densite_idees__.items():
        cle_densite = f'Densite_idees_{cle}'
        output_data[cle_densite] = valeur
        
    # Itérez à travers le dictionnaire dict_info_contenu_T_or_F et ajoutez chaque mot comme une clé avec sa valeur TRUE ou FALSE
    for mot, valeur in dict_info_contenu_T_or_F.items():
        output_data[mot] = valeur
    
    # Ajouter les informations de dépendance syntaxique
    output_data = add_dependency_info(output_data, dependance_absolu, dependance_relative)
    
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
    
    print("-" * 80)
    print(f"Le fichier {output_name} a été enregistré dans le dossier {output_dir}. L'extraction des diverses variables est finie.")


if __name__ == "__main__":
    main()