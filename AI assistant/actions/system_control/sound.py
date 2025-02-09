import os

def handle_sound_command(variables):
    """
    Ajuste le volume du système en fonction des variables extraites de la commande utilisateur.

    Args:
        variables (dict): Dictionnaire contenant les clés 'sound_level' et 'sound_adjust'.

    Returns:
        str: Résultat de l'opération ou message d'erreur.
    """
    sound_level = variables.get("sound_level")
    sound_adjust = variables.get("sound_adjust")

    if sound_level is not None:
        # Réglage direct à un niveau spécifique
        if 0 <= sound_level <= 100:
            try:
                os.system(f"amixer -D pulse sset Master {sound_level}%")
                return f"Volume réglé à {sound_level}%. "
            except Exception as e:
                return f"Échec du réglage du volume : {e}"
        return "Le niveau du volume doit être compris entre 0 et 100."
    
    elif sound_adjust == "increase":
        try:
            os.system("amixer -D pulse sset Master 5%+")
            return "Volume augmenté de 5%."
        except Exception as e:
            return f"Échec de l'augmentation du volume : {e}"
    
    elif sound_adjust == "decrease":
        try:
            os.system("amixer -D pulse sset Master 5%-")
            return "Volume diminué de 5%."
        except Exception as e:
            return f"Échec de la diminution du volume : {e}"

    return "Aucune commande de volume valide détectée."


def mute_volume():
    """
    Coupe le son du système.
    """
    try:
        os.system("amixer -D pulse sset Master mute")
        return "Volume du système coupé."
    except Exception as e:
        return f"Échec de la coupure du volume : {e}"


def unmute_volume():
    """
    Restaure le son du système.
    """
    try:
        os.system("amixer -D pulse sset Master unmute")
        return "Volume du système rétabli."
    except Exception as e:
        return f"Échec de la restauration du volume : {e}"
