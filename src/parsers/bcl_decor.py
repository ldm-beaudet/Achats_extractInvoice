"""
Parser pour les factures BCL Decor
"""
import pdfplumber
import re
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class BCLDecorParser(BaseInvoiceParser):
    """Parser pour les factures BCL Decor"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "BCL DECOR"
    
    def can_parse(self, text_content):
        """Détecte si c'est une facture BCL Decor"""
        return 'BCL' in text_content.upper() and 'AUXERRE' in text_content
    
    def extract(self, pdf_path):
        """Extrait les données d'une facture BCL Decor"""
        invoice_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    
                    for line in lines:
                        # Pattern BCL Decor : REF DESIGNATION QTE UNITE PRIX_BASE REMISE PRIX_NET MONTANT
                        # Ex: 144015 BACHE DULYFIX PLASTIFIEE 1X50M AUTOADHESIVE 1,00 U 87,94 26,09 65,00 65,00
                        
                        # Chercher lignes avec pattern complet
                        match = re.search(
                            r'^([A-Z0-9]+)\s+(.+?)\s+([\d,\.]+)\s+([A-Z]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)$',
                            line.strip()
                        )
                        
                        if match:
                            reference = match.group(1)
                            designation = match.group(2).strip()
                            quantite = clean_number(match.group(3))
                            unite = match.group(4)
                            prix_base = clean_number(match.group(5))
                            remise = clean_number(match.group(6))
                            prix_net = clean_number(match.group(7))
                            montant = clean_number(match.group(8))
                            
                            if reference and designation and quantite and montant:
                                invoice_data.append({
                                    'Fournisseur': self.supplier_name,
                                    'Fichier': Path(pdf_path).name,
                                    'Page': page_num,
                                    'Référence': reference,
                                    'Désignation': designation,
                                    'Quantité': quantite,
                                    'Unité': unite,
                                    'Prix unitaire HT': prix_base,
                                    'Remise %': remise,
                                    'Prix unitaire net': prix_net,
                                    'Montant HT': montant
                                })
        
        except Exception as e:
            print(f"Erreur BCL Decor: {e}")
        
        return invoice_data
