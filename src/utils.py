"""
Fonctions utilitaires communes à tous les parsers
"""
import re


def clean_number(value):
    """
    Nettoie et convertit une valeur en nombre
    
    Args:
        value: Valeur à convertir (str, int, float, ou None)
        
    Returns:
        float ou None: Nombre converti ou None si impossible
    """
    if value is None or value == '':
        return None
    
    value_str = str(value).strip()
    
    if not value_str or value_str == '*':
        return None
    
    # Supprimer tous les caractères sauf chiffres, virgules, points et signe moins
    value_str = re.sub(r'[^\d,.\-]', '', value_str)
    
    if not value_str:
        return None
    
    # Remplacer virgule par point (format français → international)
    value_str = value_str.replace(',', '.')
    
    try:
        return float(value_str)
    except ValueError:
        return None


def extract_first_page_text(pdf_path):
    """
    Extrait le texte de la première page d'un PDF
    
    Args:
        pdf_path: Chemin vers le PDF
        
    Returns:
        str: Texte extrait ou chaîne vide si échec
    """
    import pdfplumber
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if len(pdf.pages) > 0:
                return pdf.pages[0].extract_text() or ''
    except Exception:
        pass
    
    return ''
