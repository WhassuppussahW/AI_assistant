# actions/applications/open_app.py
import platform
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

APP_ALIASES = {
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    "spotify": "spotify",
    "chrome": "google-chrome"  # Pour Linux
}

def get_application_path(app_name):
    """
    Récupère le chemin d'accès ou la commande d'une application basée sur l'alias.
    """
    return APP_ALIASES.get(app_name.lower(), app_name)

def add_app_alias(app_name, app_path):
    """
    Ajoute ou met à jour un alias d'application dans le dictionnaire APP_ALIASES.
    """
    APP_ALIASES[app_name.lower()] = app_path
    logging.info(f"Alias ajouté : {app_name} -> {app_path}")

def open_application(app_name):
    """
    Ouvre une application en fonction de son nom ou de son alias.
    """
    system = platform.system()
    app_path = get_application_path(app_name)

    try:
        if system == "Windows":
            subprocess.Popen(app_path, shell=True)
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", app_path])
        elif system == "Linux":
            if "/" in app_path or "." in app_path:  # Chemin ou commande spécifique
                subprocess.Popen(app_path.split())
            else:
                subprocess.Popen(["xdg-open", app_path])
        else:
            return "Système d'exploitation non supporté."

        logging.info(f"L'application {app_name} a été ouverte avec succès.")
        return f"L'application {app_name} a été ouverte avec succès."
    except FileNotFoundError:
        logging.error(f"Application introuvable : {app_name} (alias : {app_path})")
        return f"Application {app_name} introuvable."
    except Exception as e:
        logging.exception(f"Erreur lors de l'ouverture de l'application {app_name}")
        return f"Erreur : {str(e)}"

# Exemple d'utilisation
if __name__ == "__main__":
    print(open_application("chrome"))
    add_app_alias("notepad", "notepad")
    print(open_application("notepad"))
