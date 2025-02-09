import requests

def ask_question(query, model_endpoint, max_tokens=100):
    """
    Envoie une question au modèle LLM et retourne la réponse.
    """
    payload = {"prompt": query, "max_tokens": max_tokens}
    try:
        response = requests.post(model_endpoint, json=payload)
        response.raise_for_status()  # Cette ligne déclenche une exception pour les erreurs HTTP
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion ou de requête : {str(e)}"
    except Exception as e:
        return f"Erreur dans le module de question : {str(e)}"

def handle_question_command(command, model_endpoint):
    """
    Extrait et traite une commande de question pour l'envoi au LLM.
    """
    if "demande" in command or "question" in command or "pose" in command:
        # Extraction de la question, ici on est plus flexible avec différentes formulations
        query = command.split("demande", 1)[-1].strip() if "demande" in command else \
                command.split("question", 1)[-1].strip() if "question" in command else \
                command.split("pose", 1)[-1].strip()

        if query:
            return ask_question(query, model_endpoint)
        else:
            return "Aucune question valide détectée dans la commande."

    return "Commande de question non reconnue."
