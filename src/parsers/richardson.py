"""
Parser pour les factures Richardson
"""
import pdfplumber
import re
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class RichardsonParser(BaseInvoiceParser):
    """Parser pour les factures Richardson"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "RICHARDSON"
    
    def can_parse(self, text_content):
        """Détecte si c'est une facture Richardson"""
        return 'RICHARDSON' in text_content.upper()
    
    def extract(self, pdf_path):
        """Extrait les données d'une facture Richardson"""
        invoice_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    
                    for line in lines:
                        if len(line) < 20:
                            continue
                        
                        # Pattern Richardson : DESIGNATION U ... ... PRIX QTE ...MONTANT CODE
                        match = re.search(
                            r'([\w\s\-/\.]+?)\s+U\s+\.+\s+\.+\s+([\d,\.]+)\s+(\d+)\s+\.+([\d,\.]+)\s+(\w+)',
                            line
                        )
                        
                        if match:
                            designation = match.group(1).strip()
                            prix_unitaire = clean_number(match.group(2))
                            quantite = clean_number(match.group(3))
                            montant = clean_number(match.group(4))
                            code = match.group(5).strip()
                            
                            # Filtrer les lignes parasites
                            if 'ECOPARTICIPATION' not in designation.upper() and \
                               'FRAIS DE PORT' not in designation.upper() and \
                               quantite and montant and montant > 1:
                                
                                invoice_data.append({
                                    'Fournisseur': self.supplier_name,
                                    'Fichier': Path(pdf_path).name,
                                    'Page': page_num,
                                    'Référence': code,
                                    'Désignation': designation,
                                    'Quantité': quantite,
                                    'Prix tarif': prix_unitaire,
                                    'Montant HT': montant
                                })
        
        except Exception as e:
            print(f"Erreur Richardson: {e}")
        
        return invoice_data
