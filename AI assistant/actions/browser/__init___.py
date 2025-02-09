# ai_assistant/actions/browser/__init__.py
import logging
from .favoris import open_favorite_page
from .search import perform_web_search

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Map intents to functions
BROWSER_COMMANDS = {
    "favori": open_favorite_page,
    "barre des favoris": open_favorite_page,
    "cherche": perform_web_search,
    "recherche": perform_web_search
}

def handle_browser_command(command):
    """
    Gère les commandes relatives au navigateur.
    """
    # Analyse simple des commandes
    for keyword, action in BROWSER_COMMANDS.items():
        if keyword in command:
            logging.info(f"Commande navigateur détectée : {keyword}")
            return action(command)

    # Si aucune commande correspondante n'est trouvée
    logging.warning(f"Commande navigateur non reconnue : {command}")
    return "Commande navigateur non reconnue."
