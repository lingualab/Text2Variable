from Importation_JSON import *
from Merge_texte import *
from Save_JSON import *
import argparse
import os
import json

def main():
    # Créez un analyseur d'arguments en ligne de commande
    parser = argparse.ArgumentParser(description="Rassemble les interventions et enregistre au format JSON.")

    # Ajoutez des arguments pour le fichier d'entrée, le nom du fichier de sortie et le dossier de sortie
    parser.add_argument("input_name", help="Nom du fichier JSON d'entrée")
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

    # Rassembler les interventions
    new_texte = rassembler_interventions(texte_input)

    # Déterminer le nom du fichier de sortie
    if args.output_name is None:
        # Utilise le nom du participant s'il est disponible
        participant_id = texte_input["participant"].get("ID", "N/A")
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

    # Ajouter les informations de l'ID, de la langue et du texte dans le dictionnaire
    output_data = {
        "ID": participant_id,
        "Langue": texte_input["participant"].get("Langue", "N/A"),
        "Texte": new_texte
    }

    # Composez le chemin complet du fichier de sortie
    output_path = os.path.join(output_dir, output_name)

    # Enregistrer la sortie au format JSON dans le dossier spécifié
    if save_json_file(output_path, output_data):
        print(f"Le fichier JSON de sortie a été enregistré sous le nom : {output_path}")

if __name__ == "__main__":
    main()
