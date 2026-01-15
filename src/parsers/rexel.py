"""
Parser pour les factures Rexel
"""
import pdfplumber
import re
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class RexelParser(BaseInvoiceParser):
    """Parser pour les factures Rexel"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "REXEL"
    
    def can_parse(self, text_content):
        """Détecte si c'est une facture Rexel"""
        return 'REXEL' in text_content.upper()
    
    def extract(self, pdf_path):
        """Extrait les données d'une facture Rexel"""
        invoice_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    
                    for i, line in enumerate(lines):
                        # Pattern Rexel : 0010 LEG038009 302,30000 65,00 105,80500 2 U 211,61 2
                        match = re.search(
                            r'^\s*(\d{4})\s+([A-Z0-9\-]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+(\d+)\s+U\s+([\d,\.]+)',
                            line
                        )
                        
                        if match:
                            num_ligne = match.group(1)
                            reference = match.group(2)
                            prix_unitaire = clean_number(match.group(3))
                            remise = clean_number(match.group(4))
                            prix_net = clean_number(match.group(5))
                            quantite = clean_number(match.group(6))
                            montant = clean_number(match.group(7))
                            
                            # La désignation est sur la ligne suivante
                            designation = ''
                            if i + 1 < len(lines):
                                next_line = lines[i + 1].strip()
                                if not re.match(r'^[A-Z0-9\-]+$', next_line) and \
                                   'Produit non repris' not in next_line:
                                    designation = next_line
                            
                            if quantite and montant:
                                invoice_data.append({
                                    'Fournisseur': self.supplier_name,
                                    'Fichier': Path(pdf_path).name,
                                    'Page': page_num,
                                    'Référence': reference,
                                    'Désignation': designation,
                                    'Quantité': quantite,
                                    'Prix tarif': prix_unitaire,
                                    'Prix net unitaire': prix_net,
                                    'Remise %': remise,
                                    'Montant HT': montant
                                })
        
        except Exception as e:
            print(f"Erreur Rexel: {e}")
        
        return invoice_data
