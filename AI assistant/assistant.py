import speech_recognition as sr
from gtts import gTTS
import threading
import os
import importlib
import pygame
from core.context_manager import ContextManager, update_context_with_request
from core.module_context import module_context
from model.model_handler import load_local_model
from model.intent_classification import classify_intent, extract_variables
from core.prepare_prompt import prepare_prompt, process_model_outputs
import torch



# Penser à Whisper et Piper pour le TTS et STT


# Initialisation
context_manager = ContextManager()
model, tokenizer = load_local_model()
tts_queue = threading.Lock()

# Text-to-Speech avec file d'attente
def speak(text):
    def tts_task():
        with tts_queue:
            tts = gTTS(text=text, lang='fr')
            tts.save("output.mp3")
            pygame.mixer.init()
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove("output.mp3")

    threading.Thread(target=tts_task).start()

# Speech-to-Text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language='fr-FR')
            return command.lower()
        except sr.UnknownValueError:
            speak("Je n'ai pas compris. Répétez s'il vous plaît.")
            return None
        except sr.RequestError as e:
            speak("Problème de connexion au service de reconnaissance vocale.")
            print(f"Error with recognition service: {e}")
            return None

# Processus de gestion des requêtes
def process_request(user_input, context_manager):
    """
    Gère la requête utilisateur en détectant l'intention et en exécutant l'action associée.

    Args:
        user_input (str): La commande utilisateur.
        context_manager (ContextManager): Gestionnaire de contexte.

    Returns:
        str: La réponse à fournir à l'utilisateur.
    """
    try:
        # Classifier l'intention (utilise model et tokenizer du contexte si nécessaires)
        model = context_manager.get_context("model")
        tokenizer = context_manager.get_context("tokenizer")
        if not model or not tokenizer:
            return "Erreur : Modèle ou tokenizer non initialisés. Veuillez vérifier le contexte."

        intent = classify_intent(user_input, model, tokenizer)
        
        # Extraire les variables liées à la commande utilisateur
        variables = extract_variables(user_input, intent)
        
        # Mettre à jour le contexte avec l'intention et les variables
        update_context_with_request(context_manager, intent, variables)

        # Vérifier si l'intention nécessite un prompt enrichi
        if intent in ["ask_question", "summarize", "write"]:
            prompt = prepare_prompt(user_input, context_manager)
            inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = model(**inputs)
            return process_model_outputs(outputs)  # Assurez-vous que cette fonction traite les résultats correctement.
        
        # Rechercher l'intention dans les modules disponibles
        for module, description in module_context.items():
            if intent in description["functions"]:
                func_details = description["functions"][intent]
                parameters = func_details["parameters"]

                # Préparer les arguments pour la fonction appelée
                args = {param: variables.get(param, context_manager.get_context(param)) for param in parameters}

                # Charger le module et exécuter la fonction correspondante
                try:
                    module_handler = importlib.import_module(f"actions.{module}")
                    module_action = getattr(module_handler, intent)
                    return module_action(**args)
                except Exception as e:
                    return f"Erreur lors de l'exécution de l'intention '{intent}': {str(e)}"

        # Intention non reconnue
        return "Commande non reconnue ou module non encore implémenté."
    
    except Exception as e:
        return f"Erreur dans le traitement de la commande : {str(e)}"




# Fonction principale
def main():
    speak("Bonjour, comment puis-je vous aider ?")
    context_manager = ContextManager()  # Initialisation du gestionnaire de contexte

    while True:
        user_input = listen()
        if not user_input:
            continue

        print(f"Vous avez dit : {user_input}")
        if "arrête" in user_input or "stop" in user_input:
            speak("Au revoir.")
            break

        response = process_request(user_input, context_manager)
        if response:
            speak(response)
        else:
            speak("Je n'ai pas compris la commande.")


if __name__ == "__main__":
    main()
