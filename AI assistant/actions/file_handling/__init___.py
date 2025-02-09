from .search import handle_file_search
from .open import open_file
from .extract import handle_text_extraction
from .delete import handle_file_deletion  # Ajout possible pour la suppression de fichiers
from .rename import handle_file_rename  # Ajout possible pour le renommage de fichiers

def handle_file_command(command, context=None):
    """
    Gère une commande liée aux fichiers (recherche, ouverture, extraction, suppression, renommage, etc.).
    """
    if "recherche" in command:
        return handle_file_search(command)
    
    elif "ouvre" in command:
        # Vérification que le contexte contient un fichier sélectionné avant d'ouvrir
        if context and context.get("selected_file"):
            return open_file(context.get("selected_file"))
        else:
            return "Aucun fichier sélectionné pour l'ouverture."
    
    elif "extrait" in command:
        # Vérification que le contexte contient un fichier pour l'extraction
        if context and context.get("selected_file"):
            return handle_text_extraction(command, context.get("selected_file"))
        else:
            return "Aucun fichier sélectionné pour l'extraction."
    
    # Ajout de la gestion de commandes supplémentaires (ex: suppression, renommage)
    elif "supprime" in command:
        if context and context.get("selected_file"):
            return handle_file_deletion(command, context.get("selected_file"))
        else:
            return "Aucun fichier sélectionné pour la suppression."
    
    elif "renomme" in command:
        if context and context.get("selected_file"):
            return handle_file_rename(command, context.get("selected_file"))
        else:
            return "Aucun fichier sélectionné pour le renommage."
    
    else:
        return "Commande de gestion des fichiers non reconnue."
