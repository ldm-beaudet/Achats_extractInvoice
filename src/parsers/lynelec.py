"""
Parser pour les factures Lynelec
"""
import pdfplumber
import re
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class LynelecParser(BaseInvoiceParser):
    """Parser pour les factures Lynelec"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "LYNELEC"
    
    def can_parse(self, text_content):
        """Détecte si c'est une facture Lynelec"""
        text_upper = text_content.upper()
        # Détecter par nom ou SIRET
        if 'LYNELEC' in text_upper:
            return True
        if 'FILS & CABLES' in text_upper.replace('\n', ' '):
            return True
        if '339 398 851' in text_content:  # SIRET Lynelec
            return True
        return False
    
    def extract(self, pdf_path):
        """Extrait les données d'une facture Lynelec"""
        invoice_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    
                    for i, line in enumerate(lines):
                        # Pattern Lynelec : N°ligne + Référence sur une ligne (peut contenir LOT, etc.)
                        # Ex: "100 1031500P" ou "100 1014C LOTN°FC044251" ou "100 1014C - LOT N° FC044251"
                        match_ref = re.match(r'^(\d+)\s+([A-Z0-9]+P?)\b', line.strip())
                        
                        if match_ref and i + 1 < len(lines):
                            num_ligne = match_ref.group(1)
                            reference = match_ref.group(2)
                            
                            # La ligne suivante contient les données
                            # Ex: "R2V3G1.5T500 0,500Km 551,00 275,501"
                            # Ex: "R2V1X185 0,048KM 19333,77 928,021"
                            next_line = lines[i + 1]
                            
                            # Pattern flexible pour gérer différents formats
                            match_data = re.search(
                                r'^(.+?)\s+([\d,\.]+\s*(?:Km|KM|UN|ML)?)\s+([\d,\.\s]+)\s+([\d,\.]+)\s*(\d+)\s*$',
                                next_line.strip()
                            )
                            
                            if match_data:
                                designation = match_data.group(1).strip()
                                quantite_str = match_data.group(2).strip()
                                prix_base_str = match_data.group(3).strip()
                                prix_net = clean_number(match_data.group(4))
                                
                                # Nettoyer le prix de base (peut contenir des espaces)
                                prix_base = clean_number(prix_base_str.replace(' ', ''))
                                
                                # Extraire la quantité
                                quantite = clean_number(
                                    quantite_str.replace('Km', '').replace('KM', '').replace('UN', '').replace('ML', '')
                                )
                                
                                montant = prix_net
                                
                                if quantite and montant:
                                    invoice_data.append({
                                        'Fournisseur': self.supplier_name,
                                        'Fichier': Path(pdf_path).name,
                                        'Page': page_num,
                                        'Référence': reference,
                                        'Désignation': designation,
                                        'Quantité': quantite,
                                        'Prix base': prix_base,
                                        'Montant HT': montant
                                    })
        
        except Exception as e:
            print(f"Erreur Lynelec: {e}")
        
        return invoice_data
