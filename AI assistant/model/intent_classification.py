import torch
import re
from actions.file_handling import handle_text_extraction

def classify_intent(command, model, tokenizer):
    """
    Utilise un modèle NLP pour classifier l'intention principale et les sub-intentions.

    Args:
        command (str): Commande utilisateur.
        model: Modèle NLP chargé.
        tokenizer: Tokenizer chargé.

    Returns:
        tuple: (Intention principale, Sub-intention)
    """
    # Préparer la commande pour le modèle
    inputs = tokenizer(command, return_tensors="pt", padding=True, truncation=True)
    
    # Obtenir les prédictions du modèle
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Extraire l'intention principale (classe avec la probabilité la plus élevée)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    
    # Mappage des classes à des intentions principales et leurs sub-intentions
    intent_map = {
        0: {
            "intent": "file_handling",
            "sub_intents": ["extract", "open", "search"]
        },
        1: {
            "intent": "browser",
            "sub_intents": ["favoris", "search"]
        },
        2: {
            "intent": "system_control",
            "sub_intents": ["brightness", "microphone", "power", "sound"]
        },
        3: {
            "intent": "outside",
            "sub_intents": ["question", "resume", "suggest", "write"]
        },
        4: {
            "intent": "applications",
            "sub_intents": ["open"]
        },
        5: {
            "intent": "other",
            "sub_intents": []
        }
    }

    intent_data = intent_map.get(predicted_class, {"intent": "unknown", "sub_intents": []})
    primary_intent = intent_data["intent"]
    sub_intents = intent_data["sub_intents"]
    
    # Identifier le sub-intent à partir de mots-clés
    detected_sub_intent = None
    for sub_intent in sub_intents:
        if sub_intent in command:
            detected_sub_intent = sub_intent
            break
    
    return primary_intent, detected_sub_intent or "unknown"

### Demander à chat de détailler les possibilités liées aux commandes, si on ne peut pas le rendre dynamque. Le rendre dynamique serait "words having 80% of correspondance/probability with the current words depending on the context"
                

def workflow_resume(variables):
    if variables["source"] == "document":
        # Étape 1 : Extraire le texte du document
        extracted_text = handle_text_extraction(variables.get("file_path", "opened_file"))
        variables["content"] = extracted_text

    # Étape 2 : Envoyer le texte à une IA extérieure pour résumer
    summary = send_to_external_ai(variables["content"], task="summarize")
    return summary


def workflow_suggest(variables):
    if variables["source"] == "document":
        # Étape 1 : Extraire le texte du document
        extracted_text = handle_text_extraction(variables.get("file_path", "opened_file"))
        variables["content"] = extracted_text

    # Étape 2 : Envoyer le texte à une IA extérieure pour proposer des améliorations
    suggestions = send_to_external_ai(variables["content"], task="suggest")
    return suggestions


class IntentHandler:
    """
    Classe de base pour tous les gestionnaires d'intentions.
    """
    def extract_variables(self, command, sub_intent):
        raise NotImplementedError("Cette méthode doit être implémentée par les sous-classes.")



class FileHandlingHandler(IntentHandler):
    def extract_variables(self, command, sub_intent):
        if sub_intent in ["extract", "open"]:
            file_path_match = re.search(r"(\/|\w:\\)([^\s]+)", command)
            return {"file_path": file_path_match.group() if file_path_match else None}
        elif sub_intent == "search":
            file_type_match = re.search(r"\b(pdf|docx?|txt|xls|csv|pptx?)\b", command, re.IGNORECASE)
            file_name_match = re.search(r"document|fichier\s+(\w+)", command, re.IGNORECASE)
            return {
                "type": file_type_match.group() if file_type_match else None,
                "name": file_name_match.group(1) if file_name_match else None
            }
        return {}

class BrowserHandler(IntentHandler):
    def extract_variables(self, command, sub_intent):
        if sub_intent == "favoris":
            bookmark_match = re.search(r"favori\s+(.+)", command, re.IGNORECASE) or \
                             re.search(r"ouvre\s+(.+)", command, re.IGNORECASE)
            return {"bookmark_name": bookmark_match.group(1).strip() if bookmark_match else None}
        elif sub_intent == "search":
            search_match = re.search(r"cherche\s+(.+)", command, re.IGNORECASE) or \
                           re.search(r"recherche\s+(.+)", command, re.IGNORECASE)
            return {"search_query": search_match.group(1).strip() if search_match else None}
        return {}

class ApplicationsHandler(IntentHandler): 
    def extract_variables(self, command, sub_intent):
        if sub_intent == "open":
            app_name = command.split("ouvre", 1)[-1].strip()
            return {"app_name": app_name}
        return {}

class OutsideHandler(IntentHandler):
    def extract_variables(self, command, sub_intent):
        if sub_intent == "resume":
            document_match = re.search(r"\b(document|texte|fichier|pdf|word|ouvert)\b", command, re.IGNORECASE)
            text_match = re.search(r"résume\s+(le texte|ce texte|.+)", command, re.IGNORECASE)
            return {
                "workflow": "workflow_resume",
                "source": "document" if document_match else "text",
                "content": text_match.group(1).strip() if text_match and not document_match else None
            }
        elif sub_intent == "suggest":
            document_match = re.search(r"\b(document|texte|fichier|pdf|word|ouvert)\b", command, re.IGNORECASE)
            text_match = re.search(r"propose\s+(des améliorations|.+)", command, re.IGNORECASE)
            return {
                "workflow": "workflow_suggest",
                "source": "document" if document_match else "text",
                "content": text_match.group(1).strip() if text_match and not document_match else None
            }
        elif sub_intent == "question":
            question_match = re.search(r"pose\s+(une question|.+)", command, re.IGNORECASE)
            return {"action": "question", "query": question_match.group(1).strip() if question_match else None}
        elif sub_intent == "write":
            topic_match = re.search(r"(écris|rédige)\s+(un mail|un texte|un paragraphe|.+)", command, re.IGNORECASE)
            return {"action": "write", "topic": topic_match.group(2).strip() if topic_match else None}
        return {}

class SystemControlHandler(IntentHandler):
    def extract_variables(self, command, sub_intent):
        if sub_intent == "brightness":
            brightness_match = re.search(r"(\d{1,3})\s*%", command)
            adjust_match = re.search(r"\bmonte\b|\bbaisse\b", command, re.IGNORECASE)
            return {
                "brightness_level": int(brightness_match.group(1)) if brightness_match else None,
                "brightness_adjust": "increase" if adjust_match and adjust_match.group().lower() == "monte" 
                                    else "decrease" if adjust_match else None
            }
        elif sub_intent == "sound":
            sound_match = re.search(r"(\d{1,3})\s*%", command)
            adjust_match = re.search(r"\bmonte\b|\bbaisse\b", command, re.IGNORECASE)
            return {
                "sound_level": int(sound_match.group(1)) if sound_match else None,
                "sound_adjust": "increase" if adjust_match and adjust_match.group().lower() == "monte" 
                                else "decrease" if adjust_match else None
            }
        elif sub_intent == "power":
            power_match = re.search(r"\b(éteins?|arrête|redémarre|veille|suspend)\b", command, re.IGNORECASE)
            if power_match:
                action = power_match.group().lower()
                return {
                    "power_action": "shutdown" if "étein" in action or "arrête" in action else 
                                     "restart" if "redémarre" in action else 
                                     "sleep" if "veille" in action or "suspend" in action else None
                }
            return {"power_action": None}
        elif sub_intent == "microphone":
            mic_match = re.search(r"\b(active?|désactive?|allume|éteins?)\b", command, re.IGNORECASE)
            if mic_match:
                action = mic_match.group().lower()
                return {"microphone_action": "activate" if "active" in action or "allume" in action else "deactivate"}
            return {"microphone_action": None}
        return {}


class IntentRouter:
    """
    Routeur qui associe les intentions principales aux gestionnaires correspondants.
    """
    def __init__(self):
        self.handlers = {
            "file_handling": FileHandlingHandler(),
            "browser": BrowserHandler(),
            "applications": ApplicationsHandler(),
            "outside": OutsideHandler(),
            "system_control": SystemControlHandler(),
            # Ajouter d'autres gestionnaires ici...
        }

    def extract_variables(self, command, intent, sub_intent):
        handler = self.handlers.get(intent)
        if handler:
            return handler.extract_variables(command, sub_intent)
        return {}




"""
def extract_variables(command, intent, sub_intent):
    ###
    Extrait les variables pertinentes d'une commande utilisateur en fonction de l'intention et du sub-intention.

    Args:
        command (str): Commande utilisateur.
        intent (str): Intention principale détectée.
        sub_intent (str): Sub-intention détectée.

    Returns:
        dict: Variables extraites.
    ###
    variables = {}

    if intent == "file_handling":
        if sub_intent in ["extract", "open"]:
            # Chercher un chemin de fichier dans la commande
            file_path_match = re.search(r"(\/|\w:\\)([^\s]+)", command)  # Unix ou Windows
            variables["file_path"] = file_path_match.group() if file_path_match else None
        elif sub_intent == "search":
            # Extraire le nom et le type de fichier
            file_type_match = re.search(r"\b(pdf|docx?|txt|xls|csv|pptx?)\b", command, re.IGNORECASE)
            file_name_match = re.search(r"document|fichier\s+(\w+)", command, re.IGNORECASE)
            variables["type"] = file_type_match.group() if file_type_match else None
            variables["name"] = file_name_match.group(1) if file_name_match else None

    elif intent == "browser":
        if sub_intent == "favoris":
            # Extraire le nom du favori
            bookmark_match = re.search(r"favori\s+(.+)", command, re.IGNORECASE) or \
                             re.search(r"ouvre\s+(.+)", command, re.IGNORECASE)
            variables["bookmark_name"] = bookmark_match.group(1).strip() if bookmark_match else None
        elif sub_intent == "search":
            # Extraire la requête de recherche
            search_match = re.search(r"cherche\s+(.+)", command, re.IGNORECASE) or \
                           re.search(r"recherche\s+(.+)", command, re.IGNORECASE)
            variables["search_query"] = search_match.group(1).strip() if search_match else None

    elif intent == "system_control":
        if sub_intent == "brightness":
            # Extraire un pourcentage ou un ajustement
            brightness_match = re.search(r"(\d{1,3})\s*%", command)  # Recherche un pourcentage
            adjust_match = re.search(r"\bmonte\b|\bbaisse\b", command, re.IGNORECASE)  # Recherche monte/baisse
            if brightness_match:
                variables["brightness_level"] = int(brightness_match.group(1))
            elif adjust_match:
                variables["brightness_adjust"] = "increase" if adjust_match.group().lower() == "monte" else "decrease"
            else:
                variables["brightness_level"] = None
                variables["brightness_adjust"] = None
        elif sub_intent == "sound":
            # Extraire un pourcentage ou un ajustement
            sound_match = re.search(r"(\d{1,3})\s*%", command)  # Recherche un pourcentage
            adjust_match = re.search(r"\bmonte\b|\bbaisse\b", command, re.IGNORECASE)
            if sound_match:
                variables["sound_level"] = int(sound_match.group(1))
            elif adjust_match:
                variables["sound_adjust"] = "increase" if adjust_match.group().lower() == "monte" else "decrease"
            else:
                variables["sound_level"] = None
                variables["sound_adjust"] = None
        elif sub_intent == "power":
            # Extraire une action liée à l'état de l'appareil
            power_match = re.search(r"\b(éteins?|arrête|redémarre|veille|suspend)\b", command, re.IGNORECASE)
            if power_match:
                action = power_match.group().lower()
                if "étein" in action or "arrête" in action:
                    variables["power_action"] = "shutdown"
                elif "redémarre" in action:
                    variables["power_action"] = "restart"
                elif "veille" in action or "suspend" in action:
                    variables["power_action"] = "sleep"
            else:
                variables["power_action"] = None
        elif sub_intent == "microphone":
            # Extraire une action liée au microphone
            mic_match = re.search(r"\b(active?|désactive?|allume|éteins?)\b", command, re.IGNORECASE)
            if mic_match:
                action = mic_match.group().lower()
                variables["microphone_action"] = "activate" if "active" in action or "allume" in action else "deactivate"
            else:
                variables["microphone_action"] = None

    elif intent == "outside":
        if sub_intent == "resume":
            variables["workflow"] = "workflow_resume"
            document_match = re.search(r"\b(document|texte|fichier|pdf|word|ouvert)\b", command, re.IGNORECASE)
            if document_match:
                variables["source"] = "document"
            else:
                text_match = re.search(r"résume\s+(le texte|ce texte|.+)", command, re.IGNORECASE)
                if text_match:
                    variables["source"] = "text"
                    variables["content"] = text_match.group(1).strip()
        elif sub_intent == "suggest":
            variables["workflow"] = "workflow_suggest"
            document_match = re.search(r"\b(document|texte|fichier|pdf|word|ouvert)\b", command, re.IGNORECASE)
            if document_match:
                variables["source"] = "document"
            else:
                text_match = re.search(r"propose\s+(des améliorations|.+)", command, re.IGNORECASE)
                if text_match:
                    variables["source"] = "text"
                    variables["content"] = text_match.group(1).strip()
        elif sub_intent == "question":
            variables["action"] = "question"
            question_match = re.search(r"pose\s+(une question|.+)", command, re.IGNORECASE)
            if question_match:
                variables["query"] = question_match.group(1).strip()
        elif sub_intent == "write":
            variables["action"] = "write"
            topic_match = re.search(r"(écris|rédige)\s+(un mail|un texte|un paragraphe|.+)", command, re.IGNORECASE)
            if topic_match:
                variables["topic"] = topic_match.group(2).strip()

    elif intent == "applications":
        if sub_intent == "open":
            variables["app_name"] = command.split("ouvre", 1)[-1].strip()

    return variables
"""