"""
Parser pour les factures Point P
"""
import pdfplumber
import re
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class PointPParser(BaseInvoiceParser):
    """Parser pour les factures Point P"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "POINT P"
    
    def can_parse(self, text_content):
        """Détecte si c'est une facture Point P"""
        return 'POINT' in text_content.upper() and ('POINT P' in text_content or 'POINT.P' in text_content)
    
    def extract(self, pdf_path):
        """Extrait les données d'une facture Point P"""
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
                        
                        # La table Point P est condensée comme SFIC
                        # Structure: [CODE\nCODE\nCODE, NOMBRE, DESIGNATION\nDESIGNATION, QUANTITE\nQUANTITE, UV, PRIX, MONTANT, TVA]
                        
                        for row in table[1:]:  # Skip header
                            if not row or not row[0]:
                                continue
                            
                            # Extraire les codes articles (première colonne)
                            codes_cell = str(row[0]).strip()
                            codes = [c.strip() for c in codes_cell.split('\n') if c.strip() and c.strip().isdigit() or re.match(r'^[A-Z0-9]+$', c.strip())]
                            
                            # Extraire les nombres (colonne NOMBRE)
                            nombres_cell = str(row[2]) if len(row) > 2 else ''
                            nombres = [clean_number(n) for n in nombres_cell.split('\n') if n.strip() and re.match(r'^[\d,\.]+$', n.strip())]
                            
                            # Extraire les désignations (colonne DESIGNATION)
                            designations_cell = str(row[4]) if len(row) > 4 else ''
                            designations_lines = designations_cell.split('\n')
                            
                            # Filtrer les désignations (ignorer lignes parasites)
                            designations = []
                            for line in designations_lines:
                                line = line.strip()
                                # Ignorer les lignes "Dont éco-contribution" et autres parasites
                                if line and not line.startswith('Dont éco-') and not line.startswith('Point.P') and not line.startswith('Les éventuels') and 'BON' not in line and 'Ref.' not in line and 'Chantier' not in line:
                                    # Ne garder que si ça ressemble à une désignation produit
                                    if len(line) > 5 and not line.startswith('0.800'):
                                        designations.append(line)
                            
                            # Extraire quantités (colonne QUANTITE)
                            quantites_cell = str(row[6]) if len(row) > 6 else ''
                            quantites_lines = quantites_cell.split('\n')
                            quantites = []
                            unites = []
                            for line in quantites_lines:
                                parts = line.split()
                                if len(parts) >= 1:
                                    q = clean_number(parts[0])
                                    if q:
                                        quantites.append(q)
                            
                            # Extraire unités (colonne UV)
                            unites_cell = str(row[8]) if len(row) > 8 else ''
                            unites = [u.strip() for u in unites_cell.split('\n') if u.strip() and len(u.strip()) <= 5]
                            
                            # Extraire prix unitaires
                            prix_cell = str(row[14]) if len(row) > 14 else ''
                            prix = [clean_number(p) for p in prix_cell.split('\n') if p.strip() and re.match(r'^[\d,\.]+$', p.strip())]
                            
                            # Extraire montants
                            montants_cell = str(row[16]) if len(row) > 16 else ''
                            montants = [clean_number(m) for m in montants_cell.split('\n') if m.strip() and re.match(r'^[\d,\.]+$', m.strip())]
                            
                            # Construire les lignes d'articles
                            max_len = max(len(codes), len(designations), len(quantites), len(montants))
                            
                            for i in range(max_len):
                                if i < len(codes) and i < len(designations) and i < len(montants):
                                    code = codes[i] if i < len(codes) else ''
                                    designation = designations[i] if i < len(designations) else ''
                                    quantite = quantites[i] if i < len(quantites) else None
                                    unite = unites[i] if i < len(unites) else ''
                                    prix_unitaire = prix[i] if i < len(prix) else None
                                    montant = montants[i] if i < len(montants) else None
                                    
                                    if code and designation and montant:
                                        invoice_data.append({
                                            'Fournisseur': self.supplier_name,
                                            'Fichier': Path(pdf_path).name,
                                            'Page': page_num,
                                            'Référence': code,
                                            'Désignation': designation,
                                            'Quantité': quantite,
                                            'Unité': unite,
                                            'Prix unitaire HT': prix_unitaire,
                                            'Montant HT': montant
                                        })
        
        except Exception as e:
            print(f"Erreur Point P: {e}")
        
        return invoice_data
