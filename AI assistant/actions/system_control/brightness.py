import subprocess

def handle_brightness_command(variables):
    """
    Ajuste la luminosité en fonction des variables extraites de la commande utilisateur.

    Args:
        variables (dict): Dictionnaire contenant les clés 'brightness_level' et 'brightness_adjust'.

    Returns:
        str: Résultat de l'opération ou message d'erreur.
    """
    brightness_level = variables.get("brightness_level")
    brightness_adjust = variables.get("brightness_adjust")

    if brightness_level is not None:
        # Ajuster directement à un niveau spécifique
        if 0 <= brightness_level <= 100:
            try:
                subprocess.run(["xrandr", "--output", "eDP-1", "--brightness", str(brightness_level / 100)], check=True)
                return f"Luminosité réglée à {brightness_level}%."
            except Exception as e:
                return f"Échec de l'ajustement de la luminosité : {e}"
        return "Le niveau de luminosité doit être compris entre 0 et 100."
    
    elif brightness_adjust == "increase":
        return "Commande pour augmenter la luminosité reçue, mais niveau non spécifié."
    
    elif brightness_adjust == "decrease":
        return "Commande pour diminuer la luminosité reçue, mais niveau non spécifié."

    return "Aucune commande de luminosité valide détectée."
