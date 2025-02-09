from transformers import AutoTokenizer, AutoModelForSequenceClassification

def load_local_model(model_name="camembert-base", context_manager=None):
    """
    Charge le modèle et le tokenizer spécifiés, avec gestion de contexte optionnelle.

    Args:
        model_name (str): Nom du modèle à charger (par défaut "camembert-base").
        context_manager (ContextManager, optional): Gestionnaire de contexte pour stocker le modèle et le tokenizer.

    Returns:
        tuple: Le modèle et le tokenizer chargés.
    """
    try:
        print(f"Chargement du modèle et du tokenizer pour {model_name}...")
        
        # Charger le tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            print(f"Info: Le token PAD manquant a été défini comme {tokenizer.eos_token}.")

        # Charger le modèle
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        # Ajouter au contexte si disponible
        if context_manager:
            context_manager.update_context("model", model)
            context_manager.update_context("tokenizer", tokenizer)

        print(f"Modèle et tokenizer pour {model_name} chargés avec succès.")
        return model, tokenizer
    except Exception as e:
        raise RuntimeError(f"Erreur lors du chargement du modèle ou du tokenizer pour {model_name}: {e}")
