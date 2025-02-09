import speech_recognition as sr

def list_microphones():
    # Liste tous les périphériques d'enregistrement audio
    microphones = sr.Microphone.list_microphone_names()
    print("Microphones disponibles :")
    for i, microphone in enumerate(microphones):
        print(f"{i}: {microphone}")
        
    return microphones

def test_microphone():
    # Essayer de détecter et d'enregistrer du son à partir du premier micro disponible
    microphones = list_microphones()
    
    if len(microphones) > 0:
        recognizer = sr.Recognizer()
        mic = sr.Microphone(device_index=0)  # Sélectionner le premier microphone
        with mic as source:
            try:
                print("Écoute...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=3)
                print("Audio capté!")
                if not audio.frame_data:  # Vérifie si l'audio est vide
                    print("Aucun son capté. Veuillez vérifier le microphone.")
                    return

                print("Reconnaissance vocale en cours...")
                command = recognizer.recognize_google(audio, language="fr-FR")
                print(f"Commande reconnue: {command}")
            except sr.WaitTimeoutError:
                print("Aucun son détecté dans le délai imparti.")
            except sr.UnknownValueError:
                print("Je n'ai pas compris.")
            except sr.RequestError as e:
                print(f"Erreur de service : {e}")


# Lancer le test
test_microphone()
