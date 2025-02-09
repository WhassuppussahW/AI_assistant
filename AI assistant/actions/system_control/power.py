import os
import platform

def shutdown():
    """
    Éteint le système.
    """
    try:
        if platform.system() == "Linux":
            os.system("shutdown now")
            return "Système en cours d'arrêt."
        else:
            return "L'arrêt du système n'est supporté que sur les systèmes Linux."
    except Exception as e:
        return f"Échec de l'arrêt du système : {e}"

def restart():
    """
    Redémarre le système.
    """
    try:
        if platform.system() == "Linux":
            os.system("reboot")
            return "Système en cours de redémarrage."
        else:
            return "Le redémarrage du système n'est supporté que sur les systèmes Linux."
    except Exception as e:
        return f"Échec du redémarrage du système : {e}"

def sleep():
    """
    Met le système en veille.
    """
    try:
        if platform.system() == "Linux":
            os.system("systemctl suspend")
            return "Système en veille."
        else:
            return "La mise en veille n'est supportée que sur les systèmes Linux."
    except Exception as e:
        return f"Échec de la mise en veille du système : {e}"

def handle_power_command(command):
    """
    Gère les commandes liées à l'alimentation.
    """
    if "éteindre" in command or "arrêter" in command:
        return shutdown()
    elif "redémarrer" in command:
        return restart()
    elif "veille" in command or "suspendre" in command:
        return sleep()
    return "Commande d'alimentation non reconnue."
