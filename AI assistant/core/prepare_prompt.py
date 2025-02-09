from core.module_context import module_context
from core.context_manager import ContextManager
import torch 

def prepare_prompt(user_input, context_manager):
    module_context = context_manager.get_context("module_context", default={})
    if not isinstance(module_context, dict):
        return "Erreur : Le contexte de module est invalide ou manquant."

    try:
        context_description = "\n".join(
            [
                f"{module}:\n  Description: {details.get('description', 'Description non disponible')}\n" +
                "\n".join(
                    [
                        f"    - {func} : {func_details.get('description', 'Description non disponible')}"
                        for func, func_details in details.get("functions", {}).items()
                    ]
                ) if "functions" in details else "    Aucune fonction disponible."
                for module, details in module_context.items()
            ]
        )
    except Exception as e:
        return f"Erreur lors de la préparation du prompt : {str(e)}"

    return f"""
Vous êtes un assistant intelligent avec les capacités suivantes :
{context_description}

Demande utilisateur : {user_input}
"""



def process_model_outputs(outputs, class_mapping=None):
    logits = getattr(outputs, "logits", None)
    if logits is None:
        return "Erreur : Les logits sont manquants dans les sorties du modèle."

    probabilities = torch.softmax(logits, dim=1)
    predicted_class_idx = torch.argmax(probabilities, dim=1).item()
    probability = probabilities[0][predicted_class_idx].item()

    predicted_class = class_mapping.get(predicted_class_idx, str(predicted_class_idx)) if class_mapping else str(predicted_class_idx)
    return f"Classe prédite: {predicted_class}, Probabilité: {probability:.2f}"
