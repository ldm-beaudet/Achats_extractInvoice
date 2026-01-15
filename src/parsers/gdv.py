"""
Parser pour les factures GDV (Le Distributeur Courants Faibles)
"""
import pdfplumber
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class GDVParser(BaseInvoiceParser):
    """Parser pour les factures GDV"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "GDV"
    
    def can_parse(self, text_content):
        """Détecte si c'est une facture GDV"""
        if 'Distributeur Courants Faibles' in text_content:
            return True
        text_upper = text_content.upper()
        if ('DISTRIBUTEUR' in text_upper and 'COURANTS' in text_upper and 'FAIBLES' in text_upper):
            return True
        return False
    
    def extract(self, pdf_path):
        """Extrait les données d'une facture GDV"""
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
                        
                        header_indices = {}
                        
                        for row in table:
                            if not row:
                                continue
                            
                            if not header_indices and self._is_header_row(row):
                                header_indices = self._find_header_indices(row)
                                continue
                            
                            if header_indices and self._has_article_data(row):
                                article = self._extract_article(row, header_indices, pdf_path, page_num)
                                if article:
                                    invoice_data.append(article)
        
        except Exception as e:
            print(f"Erreur GDV: {e}")
        
        return invoice_data
    
    def _is_header_row(self, row):
        """Vérifie si la ligne est un en-tête"""
        if not row:
            return False
        row_text = ' '.join([str(cell).lower() for cell in row if cell])
        keywords = ['référence', 'designation', 'quantité', 'prix', 'montant']
        return any(keyword in row_text for keyword in keywords)
    
    def _find_header_indices(self, row):
        """Trouve les indices des colonnes"""
        indices = {}
        
        for idx, cell in enumerate(row):
            if not cell:
                continue
            
            cell_lower = str(cell).lower().strip()
            
            if 'référence' in cell_lower:
                indices['reference'] = idx
            elif 'désignation' in cell_lower or 'designation' in cell_lower:
                indices['designation'] = idx
            elif 'qté' in cell_lower or 'quantité' in cell_lower:
                indices['quantite'] = idx
            elif 'prix tarif' in cell_lower:
                indices['prix_tarif'] = idx
            elif 'montant ht' in cell_lower or 'montant' in cell_lower:
                indices['montant_ht'] = idx
        
        return indices
    
    def _has_article_data(self, row):
        """Vérifie si la ligne contient des données d'article"""
        if not row or len(row) < 4:
            return False
        numeric_count = sum(1 for cell in row if cell and clean_number(cell) is not None)
        return numeric_count >= 2
    
    def _extract_article(self, row, header_indices, pdf_path, page_num):
        """Extrait un article d'une ligne"""
        reference = row[header_indices.get('reference', 0)] if header_indices.get('reference') is not None else ''
        designation = row[header_indices.get('designation', 2)] if header_indices.get('designation') is not None else ''
        quantite = clean_number(row[header_indices.get('quantite', 7)]) if header_indices.get('quantite') is not None else None
        prix_tarif = clean_number(row[header_indices.get('prix_tarif', 8)]) if header_indices.get('prix_tarif') is not None else None
        montant_ht = clean_number(row[header_indices.get('montant_ht', 11)]) if header_indices.get('montant_ht') is not None else None
        
        if (designation or reference) and quantite is not None and montant_ht is not None:
            return {
                'Fournisseur': self.supplier_name,
                'Fichier': Path(pdf_path).name,
                'Page': page_num,
                'Référence': str(reference).strip() if reference else '',
                'Désignation': str(designation).strip() if designation else '',
                'Quantité': quantite,
                'Prix tarif': prix_tarif,
                'Montant HT': montant_ht
            }
        
        return None
