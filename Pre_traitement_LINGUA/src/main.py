from load_models import SpaCyModelLoader
from Importation_JSON import read_json_file
from Nettoyage_du_texte import nettoyer_texte
from Tokenisation import tokeniser_texte
from Suppression_des_stops_words import supprimer_stop_words
from Lemmatisation import lemmatiser_texte
import spacy
import argparse
import os
import json

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
    data_texte = texte_input.get("Texte", "N/A")
    
    
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

    texte_nettoye = nettoyer_texte(data_texte)
    tokens = tokeniser_texte(texte_nettoye,  model)
    tokens_sans_stop = supprimer_stop_words(tokens,  model)
    lemmes = lemmatiser_texte(texte_nettoye,  model)


    # Ajouter les informations au dictionnaire de sortie
    output_data = {
        "ID": participant_id,
        "Langue": texte_input.get("Langue", "N/A"),
        "SpaCy_Model" : nom_du_modele,
        "Texte_original": data_texte,
        "Texte_nettoye": texte_nettoye,
        "Texte_tokenizes": tokens,
        "Texte_tokenizes_sans_stop": tokens_sans_stop,
        "Lemmes": lemmes,
        
    }
    
    # Composez le chemin complet du fichier de sortie
    output_path = os.path.join(output_dir, output_name)
    
    # Enregistrez le fichier JSON de sortie
    # Convertir le dictionnaire en format JSON avec une indentation pour chaque élément
    output_json = json.dumps(output_data, indent=4)

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path + "_clean.json", "w") as json_file:
        json_file.write(output_json)
    
    print(f"Le fichier {output_name} a été enregistré dans le dossier {output_dir}. Le prétraitement est terminé.")


if __name__ == "__main__":
    main()