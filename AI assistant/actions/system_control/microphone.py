import os
import platform

def mute_microphone():
    """
    Coupe le microphone.
    """
    try:
        if platform.system() == "Linux":
            os.system("amixer set Capture nocap")
            return "Microphone coupé."
        else:
            return "La coupure du microphone n'est supportée que sur les systèmes Linux."
    except Exception as e:
        return f"Échec de la coupure du microphone : {e}"

def unmute_microphone():
    """
    Réactive le microphone.
    """
    try:
        if platform.system() == "Linux":
            os.system("amixer set Capture cap")
            return "Microphone réactivé."
        else:
            return "La réactivation du microphone n'est supportée que sur les systèmes Linux."
    except Exception as e:
        return f"Échec de la réactivation du microphone : {e}"

def handle_microphone_command(command):
    """
    Gère les commandes liées au microphone.
    """
    if "microphone" in command:
        if "mute" in command or "couper" in command:
            return mute_microphone()
        elif "unmute" in command or "réactiver" in command:
            return unmute_microphone()
    return "Commande microphone non reconnue. Essayez de dire 'couper le microphone' ou 'réactiver le microphone'."
