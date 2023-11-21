def rassembler_interventions(data):
    """
    Rassemble le contenu des interventions à partir des données JSON fournies.

    Args:
        data (dict): Un dictionnaire contenant des informations sur le participant et les interventions.

    Returns:
        str or None: Une chaîne de caractères contenant la langue, l'ID du participant et le texte complet des interventions,
        ou None en cas d'erreur.

    """
    try:
        # Récupère les informations sur le participant
        participant_info = data["participant"]
        langage = participant_info.get("Langue", "N/A")
        ID = participant_info.get("ID", "N/A")
        
        # Récupère les interventions à partir des données JSON
        interventions = data["test"]["interventions"]
        texte_complet = []

        # Parcourt chaque intervention et extrait le contenu
        for intervention in interventions:
            contenu = intervention.get("contenu", "")
            texte_complet.append(contenu)

        # Concatène le texte complet des interventions
        texte_concatene = " ".join(texte_complet)

        # Crée une chaîne de caractères résultante
        resultat = texte_concatene

        return resultat
    except Exception as e:
        # Gère les exceptions et affiche un message d'erreur en cas de problème
        print(f"Une erreur s'est produite : {str(e)}")
        return None
