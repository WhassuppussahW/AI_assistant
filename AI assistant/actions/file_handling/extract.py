from PyPDF2 import PdfReader
import docx
import os

def extract_text_from_pdf(file_path):
    """
    Extrait le texte d'un fichier PDF.
    """
    try:
        reader = PdfReader(file_path)
        text = ''.join([page.extract_text() for page in reader.pages])
        if text:
            return text
        else:
            return "Aucun texte extrait du PDF. Il peut être protégé ou mal formaté."
    except Exception as e:
        return f"Erreur lors de l'extraction du texte du PDF : {e}"

def extract_text_from_word(file_path):
    """
    Extrait le texte d'un fichier Word (.docx).
    """
    try:
        doc = docx.Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        if text:
            return text
        else:
            return "Aucun texte extrait du fichier Word. Il peut être protégé ou mal formaté."
    except Exception as e:
        return f"Erreur lors de l'extraction du texte du fichier Word : {e}"

def extract_text_from_txt(file_path):
    """
    Extrait le texte d'un fichier texte (.txt).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        if text:
            return text
        else:
            return "Le fichier texte est vide."
    except Exception as e:
        return f"Erreur lors de l'extraction du texte du fichier texte : {e}"

def handle_text_extraction(file_path):
    """
    Gère l'extraction de texte en fonction du type de fichier.
    """
    if not os.path.exists(file_path):
        return f"Le fichier {file_path} n'existe pas."

    # Extraction selon le type de fichier
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_word(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        return "Type de fichier non pris en charge pour l'extraction."
