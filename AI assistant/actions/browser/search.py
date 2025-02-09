import webbrowser
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def perform_web_search(search_query):
    """
    Effectue une recherche sur le Web à partir de la commande utilisateur.
    """
    # Vérification de la présence des mots-clés "cherche" ou "recherche"
    if "cherche" in search_query or "recherche" in search_query:
        # Extraction du terme de recherche après le mot-clé
        if "cherche" in search_query:
            query = search_query.split("cherche")[-1].strip()
        elif "recherche" in search_query:
            query = search_query.split("recherche")[-1].strip()

        # Si un terme de recherche est extrait
        if query:
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)
            logging.info(f"Recherche lancée pour : {query}")
            return f"Recherche lancée pour : {query}."
        else:
            logging.warning("Aucun terme de recherche trouvé après 'cherche' ou 'recherche'.")
            return "Aucun terme de recherche n'a été trouvé dans la commande."

    logging.warning("Aucun mot-clé de recherche ('cherche' ou 'recherche') trouvé dans la commande.")
    return "Commande de recherche non reconnue."
