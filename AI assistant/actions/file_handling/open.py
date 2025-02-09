import os
import subprocess
import platform

def open_file(file_path):
    """
    Ouvre un fichier avec l'application associée par défaut selon le système d'exploitation.
    """
    if not os.path.exists(file_path):
        return f"Le fichier {file_path} est introuvable."

    try:
        system = platform.system()
        
        if system == "Linux":
            subprocess.run(["xdg-open", file_path], check=True)  # Fonctionne sous Linux
        elif system == "Darwin":  # macOS
            subprocess.run(["open", file_path], check=True)
        elif system == "Windows":
            os.startfile(file_path)  # Fonctionne sous Windows
        else:
            return "Système d'exploitation non supporté pour ouvrir le fichier."

        return f"Fichier {file_path} ouvert avec succès."
    except Exception as e:
        return f"Erreur lors de l'ouverture du fichier {file_path} : {str(e)}"
