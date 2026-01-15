"""
Parser pour les factures Sonepar
"""
import pdfplumber
import re
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class SoneparParser(BaseInvoiceParser):
    """Parser pour les factures Sonepar"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "SONEPAR"
    
    def can_parse(self, text_content):
        """Détecte si c'est une facture Sonepar"""
        return 'SONEPAR' in text_content.upper() and 'FRANCE DISTRIBUTION' in text_content.upper()
    
    def extract(self, pdf_path):
        """Extrait les données d'une facture Sonepar"""
        invoice_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    tables = page.extract_tables()
                    
                    if not tables:
                        continue
                    
                    for table in tables:
                        if not table or len(table) < 2:
                            continue
                        
                        # Chercher l'en-tête
                        header_found = False
                        for row in table:
                            if row and any('Prix de base' in str(cell) for cell in row if cell):
                                header_found = True
                                continue
                            
                            if not header_found:
                                continue
                            
                            # Ligne d'article
                            if row and row[0]:
                                # Format Sonepar: [REF_FOURNISSEUR / REF, CODE, QTE, PRIX_BASE, REMISE, PU_NET, MONTANT]
                                # Ex: "00001404906 / 404906\nLEGRAND BORNE D'ARRIVEE POUR CABLE 35"
                                
                                first_cell = str(row[0]).strip()
                                
                                # Ignorer les lignes D3E et autres lignes parasites
                                if 'D3E' in first_cell.upper() or 'CONTRIBUTION' in first_cell.upper():
                                    continue
                                
                                # Extraire référence et désignation
                                # Pattern: "REF_FOURNISSEUR / REF_ARTICLE\nMARQUE DESIGNATION"
                                match_ref = re.search(r'(\d+)\s*/\s*([A-Z0-9]+)', first_cell)
                                
                                if match_ref:
                                    ref_fournisseur = match_ref.group(1)
                                    reference = match_ref.group(2)
                                    
                                    # Extraire la désignation (après le saut de ligne)
                                    parts = first_cell.split('\n')
                                    designation = ''
                                    if len(parts) > 1:
                                        # Prendre tout après la première ligne
                                        designation = ' '.join(parts[1:]).strip()
                                    
                                    # Extraire les données numériques
                                    code = row[1] if len(row) > 1 else ''
                                    
                                    # Quantité (peut être "4\nUN")
                                    qte_cell = row[2] if len(row) > 2 else ''
                                    qte_parts = str(qte_cell).split('\n') if qte_cell else []
                                    quantite = clean_number(qte_parts[0]) if qte_parts else None
                                    unite = qte_parts[1] if len(qte_parts) > 1 else ''
                                    
                                    prix_base = clean_number(row[3]) if len(row) > 3 else None
                                    remise = clean_number(row[4]) if len(row) > 4 else None
                                    pu_net = clean_number(row[5]) if len(row) > 5 else None
                                    
                                    # Montant (peut être "7.12\n(76)")
                                    montant_cell = row[6] if len(row) > 6 else ''
                                    montant_parts = str(montant_cell).split('\n') if montant_cell else []
                                    montant = clean_number(montant_parts[0]) if montant_parts else None
                                    
                                    if reference and designation and quantite and montant:
                                        invoice_data.append({
                                            'Fournisseur': self.supplier_name,
                                            'Fichier': Path(pdf_path).name,
                                            'Page': page_num,
                                            'Référence': reference,
                                            'Désignation': designation,
                                            'Code': code,
                                            'Quantité': quantite,
                                            'Unité': unite,
                                            'Prix base HT': prix_base,
                                            'Remise %': remise,
                                            'PU net HT': pu_net,
                                            'Montant HT': montant
                                        })
        
        except Exception as e:
            print(f"Erreur Sonepar: {e}")
        
        return invoice_data
