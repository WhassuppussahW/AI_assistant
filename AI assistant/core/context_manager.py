class ContextManager:
    """
    Une classe pour gérer le contexte de l'assistant.
    Stocke, met à jour et récupère des informations contextuelles (intention, chemins de fichiers, paramètres, etc.).
    """
    def __init__(self):
        self.context = {}

    def update_context(self, key, value):
        """
        Met à jour ou ajoute une nouvelle paire clé-valeur au contexte.
        
        :param key: La clé identifiant l'élément de contexte.
        :param value: La valeur associée à la clé.
        """
        self.context[key] = value

    def get_context(self, key, default=None):
        """
        Récupère une valeur spécifique du contexte via sa clé.
        
        :param key: La clé identifiant l'élément de contexte.
        :param default: Valeur par défaut si la clé n'existe pas.
        :return: La valeur associée ou la valeur par défaut.
        """
        return self.context.get(key, default)

    def clear_context(self):
        """
        Réinitialise toutes les variables de contexte.
        """
        self.context.clear()

    def remove_context_key(self, key):
        """
        Supprime une clé spécifique du contexte.
        
        :param key: La clé à supprimer.
        """
        if key in self.context:
            del self.context[key]

    def list_context(self):
        """
        Liste toutes les clés et valeurs actuellement stockées dans le contexte.
        
        :return: Un dictionnaire contenant tout le contexte.
        """
        return self.context

def update_context_with_request(self, intent, variables):
    """
    Met à jour le contexte avec une nouvelle intention et ses variables associées.

    Args:
        intent (str): L'intention détectée.
        variables (dict): Les variables extraites de l'intention.
    """
    self.update_context("last_intent", intent)
    self.update_context("last_variables", variables)


