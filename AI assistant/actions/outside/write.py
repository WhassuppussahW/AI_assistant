import requests

def generate_text(prompt, model_endpoint, max_tokens=300, temperature=0.7):
    """
    Envoie un prompt de génération de texte au modèle LLM et retourne le contenu généré.
    """
    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    try:
        response = requests.post(model_endpoint, json=payload)
        response.raise_for_status()  # Gère les erreurs HTTP
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion ou de requête : {str(e)}"
    except Exception as e:
        return f"Erreur dans le module de génération de texte : {str(e)}"

def handle_write_command(command, model_endpoint):
    """
    Extrait et traite une commande de génération de texte pour l'envoi au modèle LLM.
    """
    if "write" in command or "generate" in command:
        # Extraction plus robuste du prompt après les mots-clés "write" ou "generate"
        prompt = command.split("write", 1)[-1].strip() if "write" in command else \
                 command.split("generate", 1)[-1].strip()

        if prompt:
            return generate_text(prompt, model_endpoint)
        else:
            return "Aucun texte à générer trouvé dans la commande."
    
    return "Commande de génération de texte non reconnue."
