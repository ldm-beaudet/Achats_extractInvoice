"""
Parser pour les factures Clareo Lighting
"""
import pdfplumber
import re
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class ClareoParser(BaseInvoiceParser):
    """Parser pour les factures Clareo"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "CLAREO"
    
    def can_parse(self, text_content):
        """Détecte si c'est une facture Clareo"""
        text_upper = text_content.upper()
        return 'CLAREO' in text_upper and 'LIGHTING' in text_upper
    
    def extract(self, pdf_path):
        """Extrait les données d'une facture Clareo"""
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
                        
                        # Chercher le tableau avec les articles
                        header = table[0]
                        if not header or 'Référence' not in str(header):
                            continue
                        
                        if len(table) < 2:
                            continue
                        
                        data_row = table[1]
                        
                        # Extraire les cellules
                        references_cell = data_row[0] if data_row else ''
                        quantites_cell = data_row[5] if len(data_row) > 5 else ''
                        prix_cell = data_row[6] if len(data_row) > 6 else ''
                        montants_cell = data_row[7] if len(data_row) > 7 else ''
                        designations_cell = data_row[1] if len(data_row) > 1 else ''
                        
                        # Séparer les lignes
                        if references_cell:
                            references = [r.strip() for r in str(references_cell).split('\n') if r.strip()]
                            quantites = [q.strip() for q in str(quantites_cell).split('\n') if q.strip()]
                            prix = [p.strip() for p in str(prix_cell).split('\n') if p.strip()]
                            montants = [m.strip() for m in str(montants_cell).split('\n') if m.strip()]
                            
                            designations_text = str(designations_cell) if designations_cell else ''
                            designations = self._extract_designations(designations_text, len(references))
                            
                            # Combiner les données
                            for i in range(len(references)):
                                if i < len(references):
                                    reference = references[i]
                                    designation = designations[i] if i < len(designations) else ''
                                    quantite = clean_number(quantites[i]) if i < len(quantites) else None
                                    prix_unit = clean_number(prix[i]) if i < len(prix) else None
                                    montant = clean_number(montants[i]) if i < len(montants) else None
                                    
                                    if reference and quantite and montant:
                                        invoice_data.append({
                                            'Fournisseur': self.supplier_name,
                                            'Fichier': Path(pdf_path).name,
                                            'Page': page_num,
                                            'Référence': reference,
                                            'Désignation': designation,
                                            'Quantité': quantite,
                                            'Prix unitaire HT': prix_unit,
                                            'Montant HT': montant
                                        })
        
        except Exception as e:
            print(f"Erreur Clareo: {e}")
        
        return invoice_data
    
    def _extract_designations(self, text, expected_count):
        """Extrait les désignations du texte condensé"""
        if not text:
            return [''] * expected_count
        
        lines = text.split('\n')
        designations = []
        current_designation = []
        
        for line in lines:
            line = line.strip()
            
            # Arrêter aux messages parasites
            if any(keyword in line for keyword in ['Message à propos', 'ATTENTION aux FRAUDES', 'Suite à des problèmes']):
                break
            
            if not line:
                continue
            
            # Détecter début d'article
            if re.match(r'^[A-Z][a-z]+\s+[A-Z]', line) or re.match(r'^Driver', line):
                if current_designation:
                    designations.append(' '.join(current_designation))
                    current_designation = []
                current_designation.append(line)
            else:
                if current_designation or line:
                    current_designation.append(line)
        
        # Ajouter la dernière désignation
        if current_designation:
            designations.append(' '.join(current_designation))
        
        # Compléter si nécessaire
        while len(designations) < expected_count:
            designations.append('')
        
        return designations[:expected_count]
