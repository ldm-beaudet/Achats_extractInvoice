"""
Parser pour les factures Nollet
"""
import pdfplumber
import re
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class NolletParser(BaseInvoiceParser):
    """Parser pour les factures Nollet"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "NOLLET"
    
    def can_parse(self, text_content):
        """Détecte si c'est une facture Nollet"""
        # Chercher des éléments caractéristiques de Nollet
        text_upper = text_content.upper()
        # Vérifier SIRET ou nom dans le texte
        # Nollet a plusieurs SIRETs selon les agences
        if '370 501 207' in text_content:  # SIRET Nollet Montivilliers
            return True
        if '580 501 153' in text_content:  # SIRET Nollet Saint-Étienne-du-Rouvray
            return True
        if 'GINKGO BILOBA' in text_content and 'MONTIVILLIERS' in text_content:
            return True
        return False
    
    def extract(self, pdf_path):
        """Extrait les données d'une facture Nollet"""
        invoice_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    
                    i = 0
                    while i < len(lines):
                        line = lines[i].strip()
                        
                        # Pattern Nollet : REF DESIGNATION QTE PRIX UNITE MONTANT 1
                        # Ex: LEG069551L Prisedecourant2P+TPlexocomposable 1,000 393,00 CT 3,93 1
                        # Ex: P0MMYX13ZD/A iPhone16ProMax512GoTitaneblanc 1,000 1799,90 UN 1 799,90 1
                        # Note: Les nombres peuvent contenir des espaces (1 799,90)
                        match = re.search(
                            r'^([A-Z0-9/]+)\s*(.+?)\s+([\d,\.]+)\s+([\d,\.\s]+?)\s+([A-Z]{2,3})\s+([\d,\.\s]+?)\s+1\s*$',
                            line
                        )
                        
                        if match:
                            reference = match.group(1)
                            designation = match.group(2).strip()
                            quantite = clean_number(match.group(3))
                            prix_unitaire = clean_number(match.group(4))
                            unite = match.group(5)
                            montant = clean_number(match.group(6))
                            
                            # La ligne suivante peut être :
                            # - La même référence (à ignorer)
                            # - Un complément de désignation
                            if i + 1 < len(lines):
                                next_line = lines[i + 1].strip()
                                
                                # Si c'est juste la référence répétée, ignorer
                                if next_line == reference or next_line == f'1{reference}':
                                    # Vérifier la ligne d'après pour complément
                                    if i + 2 < len(lines):
                                        next_next_line = lines[i + 2].strip()
                                        # Si pas un nouvel article, c'est un complément
                                        if next_next_line and not re.match(r'^[A-Z0-9]+\s+.+\s+[\d,\.]+\s+[\d,\.]+\s+[A-Z]{2,3}\s+[\d,\.]+\s+1$', next_next_line):
                                            designation = f"{designation} {next_next_line}"
                                # Si ce n'est pas la référence et pas un nouvel article, c'est un complément
                                elif next_line and not re.match(r'^[A-Z0-9]+\s+', next_line):
                                    designation = f"{designation} {next_line}"
                            
                            if reference and quantite and montant:
                                invoice_data.append({
                                    'Fournisseur': self.supplier_name,
                                    'Fichier': Path(pdf_path).name,
                                    'Page': page_num,
                                    'Référence': reference,
                                    'Désignation': designation,
                                    'Quantité': quantite,
                                    'Unité': unite,
                                    'Prix unitaire HT': prix_unitaire,
                                    'Montant HT': montant
                                })
                        
                        i += 1
        
        except Exception as e:
            print(f"Erreur Nollet: {e}")
        
        return invoice_data
