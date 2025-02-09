import os
import re

def search_files(directories, query, file_extension=None):
    """
    Recherche des fichiers dans plusieurs répertoires donnés en fonction d'un mot-clé et/ou d'une extension de fichier.
    """
    results = []
    try:
        for directory in directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if query.lower() in file.lower() and (file_extension is None or file.endswith(file_extension)):
                        results.append(os.path.join(root, file))
    except Exception as e:
        return f"Erreur lors de la recherche dans {directory} : {str(e)}", []
    
    return results

def handle_file_search(command, context=None):
    """
    Gère une commande de recherche de fichier en fonction des variables extraites.
    """
    # Extraire les variables nécessaires du contexte ou du command
    file_type_match = re.search(r"\b(pdf|docx?|txt|xls|csv|pptx?)\b", command, re.IGNORECASE)
    file_name_match = re.search(r"document|fichier\s+(\w+)", command, re.IGNORECASE)
    
    file_extension = None
    if file_type_match:
        extensions_map = {
            "pdf": ".pdf",
            "docx": ".docx",
            "doc": ".doc",
            "txt": ".txt",
            "xls": ".xls",
            "csv": ".csv",
            "pptx": ".pptx"
        }
        file_extension = extensions_map.get(file_type_match.group().lower())
    
    query = file_name_match.group(1) if file_name_match else ""
    
    # Définir les répertoires de recherche
    search_directories = [
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Bureau"),
        os.path.expanduser("~/Téléchargements")
    ]
    
    # Effectuer la recherche
    search_results = search_files(search_directories, query, file_extension)
    
    if search_results:
        return {
            "type": file_type_match.group() if file_type_match else None,
            "name": query,
            "results": search_results
        }
    else:
        return {
            "type": file_type_match.group() if file_type_match else None,
            "name": query,
            "results": []
        }
