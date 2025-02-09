import requests

def summarize_text(text, model_endpoint, max_tokens=100):
    """
    Envoie un texte au modèle LLM pour obtenir un résumé.
    
    Args:
        text (str): Le texte à résumer.
        model_endpoint (str): L'URL de l'API du modèle LLM.
        max_tokens (int): Nombre maximum de tokens dans la réponse.

    Returns:
        str: Le résumé généré ou un message d'erreur.
    """
    payload = {"prompt": f"Résumé du texte : {text}", "max_tokens": max_tokens}
    try:
        response = requests.post(model_endpoint, json=payload)
        response.raise_for_status()  # Déclenche une exception pour les erreurs HTTP
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion ou de requête : {str(e)}"
    except Exception as e:
        return f"Erreur dans le module de résumé : {str(e)}"

def handle_resume_command(command, model_endpoint):
    """
    Extrait et traite une commande de résumé pour l'envoi au LLM.

    Args:
        command (str): La commande utilisateur contenant le texte à résumer.
        model_endpoint (str): L'URL de l'API du modèle LLM.

    Returns:
        str: Le résumé généré ou un message d'erreur.
    """
    if "résume" in command or "résumé" in command:
        # Extraction du texte à résumer après le mot clé
        text_to_summarize = command.split("résume", 1)[-1].strip() if "résume" in command else \
                            command.split("résumé", 1)[-1].strip()

        if text_to_summarize:
            return summarize_text(text_to_summarize, model_endpoint)
        else:
            return "Aucun texte valide détecté pour le résumé."

    return "Commande de résumé non reconnue."
