import spacy

class ModelNotDownloadedException(Exception):
    """Exception personnalisée levée lorsqu'un modèle n'est pas téléchargé."""
    pass

class SpaCyModelLoader:
    def __init__(self):
        """Initialise un dictionnaire vide pour stocker les modèles chargés."""
        self.models = {}
        self.model_dict = {
            "Francais": {
                "sm": "fr_core_news_sm",
                "md": "fr_core_news_md",
                "lg": "fr_core_news_lg",
                "trf": "fr_dep_news_trf",
            },
            "English": {
                "sm": "en_core_web_sm",
                "md": "en_core_web_md",
                "lg": "en_core_web_lg",
                "trf": "en_core_web_trf",
            },
        }

    def load(self, langue, model_size):
        """
        ...
        """
        if langue in self.model_dict:
            model_name = self.model_dict[langue].get(model_size)
        
            if model_name:
                alias = f"{langue.lower()}_{model_size}"
                self._load_model(model_name, alias=alias)
                self.display_loaded_models()
                return self.get_model(alias), self.models[alias]["full_name"]
            else:
                print("Taille de modèle non valide. Les tailles valides sont : sm, md, lg, trf.")
        else:
            print("Langue non reconnue, contactez l'administrateur du programme pour ajouter votre langue.")
        return None
    
    def _load_model(self, model_name: str, alias: str = None) -> None:
        """Charge le modèle SpaCy spécifié."""
        alias = alias or model_name
        try:
            model = spacy.load(model_name)
            self.models[alias] = {
                "model": model,
                "full_name": model_name
            }
        except Exception as e:
            raise ModelNotDownloadedException(f"Erreur lors du chargement du modèle '{model_name}': {e}")

    def get_model(self, alias: str):
        """Retourne le modèle chargé avec l'alias spécifié."""
        return self.models.get(alias, {}).get("model", None)

    def display_loaded_models(self) -> None:
        """Affiche tous les modèles actuellement chargés."""
        if self.models:
            print("Modèles chargés avec succès :")
            for alias, model_info in self.models.items():
                print(f"- Nom personnalisé : {alias}, Modèle : {model_info['full_name']}")
        else:
            print("Aucun modèle chargé.")



