import os
import sqlite3
import webbrowser
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def read_firefox_bookmarks():
    """
    Lit les favoris de Firefox à partir de la base de données places.sqlite.
    """
    profiles_dir = os.path.expanduser("~/.mozilla/firefox/")
    profile_dirs = [d for d in os.listdir(profiles_dir) if d.endswith(".default-release")]
    
    if not profile_dirs:
        logging.warning("Aucun profil Firefox trouvé.")
        return []
    
    profile_folder = os.path.join(profiles_dir, profile_dirs[0])
    bookmarks_db_path = os.path.join(profile_folder, "places.sqlite")

    if not os.path.exists(bookmarks_db_path):
        logging.error(f"Base de données de favoris introuvable : {bookmarks_db_path}")
        return []
    
    try:
        conn = sqlite3.connect(bookmarks_db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT moz_places.url, moz_bookmarks.title
            FROM moz_bookmarks
            JOIN moz_places ON moz_bookmarks.fk = moz_places.id
            WHERE moz_bookmarks.type = 1
        """)
        bookmarks = [(row[0], row[1]) for row in cursor.fetchall()]
        conn.close()
        return bookmarks
    except sqlite3.Error as e:
        logging.error(f"Erreur lors de la lecture de la base de données SQLite : {e}")
        return []

def open_favorite_page(bookmark_name):
    """
    Ouvre une page favorite en fonction de la commande utilisateur.
    Recherche dans les favoris par titre ou URL.
    """
    bookmarks = read_firefox_bookmarks() 
    if not bookmarks:
        return "Aucun favori trouvé ou erreur de lecture des favoris."

    # Recherche d'une page en fonction de la commande utilisateur
    for url, title in bookmarks:
        if title and title.lower() in bookmark_name.lower():
            webbrowser.open(url)
            logging.info(f"Page favorite ouverte : {title} ({url})")
            return f"Ouverture de la page favorite : {title}."
    
    logging.warning(f"Aucun favori correspondant trouvé pour le favoris : {bookmark_name}")
    return "Aucun favori correspondant trouvé."

