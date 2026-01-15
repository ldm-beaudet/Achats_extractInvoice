"""
Parser pour les factures Caparol Center
"""
import pdfplumber
import re
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class CaparolParser(BaseInvoiceParser):
    """Parser pour les factures Caparol Center"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "CAPAROL"
    
    def can_parse(self, text_content):
        """Détecte si c'est une facture Caparol"""
        text_upper = text_content.upper()
        return 'CAPAROL' in text_upper and 'DISTRIBUTEUR' in text_upper
    
    def extract(self, pdf_path):
        """Extrait les données d'une facture Caparol"""
        invoice_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    
                    for i, line in enumerate(lines):
                        # Pattern Caparol : REF DESIGNATION NBRE EMBL UNITE QTE PRIX REMISE MONTANT
                        # Ex: 854963 Primaire A936 20Kg 1 1 PCE 1 190,30 0,00 190,30
                        # Ex: 934892 DUMMY FORBO SOL 170,1 1 M2 170,1 13,40 0,00 2.279,34
                        
                        # Regex flexible pour capturer les données
                        match = re.search(
                            r'^(\d{6,})\s+(.+?)\s+([\d,\.]+)\s+(\d+)\s+(PCE|M2|L|KG)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)$',
                            line.strip()
                        )
                        
                        if match:
                            reference = match.group(1)
                            designation = match.group(2).strip()
                            nbre = clean_number(match.group(3))
                            emballage = clean_number(match.group(4))
                            unite = match.group(5)
                            quantite = clean_number(match.group(6))
                            prix_unitaire = clean_number(match.group(7))
                            remise_pct = clean_number(match.group(8))
                            montant = clean_number(match.group(9))
                            
                            # Filtrer les écocontributions
                            if 'ECO CONTRIBUTION' in designation.upper():
                                continue
                            
                            if designation and quantite and montant:
                                # Vérifier si la désignation continue sur la ligne suivante
                                designation_complete = designation
                                if i + 1 < len(lines):
                                    next_line = lines[i + 1].strip()
                                    # Si la ligne suivante ne commence pas par un chiffre, c'est probablement la suite
                                    if next_line and not re.match(r'^\d', next_line) and len(next_line) < 80:
                                        # Éviter les en-têtes
                                        if not any(keyword in next_line for keyword in ['Bon de livraison', 'Votre nº', 'Total', 'Code couleur']):
                                            designation_complete = f"{designation} {next_line}"
                                
                                invoice_data.append({
                                    'Fournisseur': self.supplier_name,
                                    'Fichier': Path(pdf_path).name,
                                    'Page': page_num,
                                    'Référence': reference,
                                    'Désignation': designation_complete,
                                    'Quantité': quantite,
                                    'Unité': unite,
                                    'Prix unitaire HT': prix_unitaire,
                                    'Remise %': remise_pct if remise_pct and remise_pct != 0 else None,
                                    'Montant HT': montant
                                })
        
        except Exception as e:
            print(f"Erreur Caparol: {e}")
        
        return invoice_data
