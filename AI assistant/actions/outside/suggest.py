import requests

def provide_suggestions(context, model_endpoint, max_tokens=200, temperature=0.7):
    """
    Envoie une requête de suggestion au modèle LLM et retourne la réponse.
    """
    prompt = f"Provide suggestions based on the following context:\n{context}"
    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    try:
        response = requests.post(model_endpoint, json=payload)
        response.raise_for_status()  # Déclenche une exception pour les erreurs HTTP
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion ou de requête : {str(e)}"
    except Exception as e:
        return f"Erreur dans le module de suggestions : {str(e)}"

def handle_suggest_command(command, model_endpoint):
    """
    Extrait et traite une commande de suggestions pour l'envoi au modèle LLM.
    """
    if "suggest" in command or "recommend" in command:
        # Extraction du contexte (texte à suggérer)
        context = command.split("suggest", 1)[-1].strip() if "suggest" in command else \
                 command.split("recommend", 1)[-1].strip()

        if context:
            return provide_suggestions(context, model_endpoint)
        else:
            return "Aucun contexte trouvé pour les suggestions."

    return "Commande de suggestion non reconnue."
