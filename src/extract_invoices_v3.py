#!/usr/bin/env python3
"""
Extracteur de factures multi-fournisseurs
Version 3.0 - Support GDV et Richardson
"""

import pdfplumber
import pandas as pd
import re
from pathlib import Path
import sys


# =====================================================
# UTILITAIRES COMMUNS
# =====================================================

def clean_number(value):
    """Nettoie et convertit une valeur en nombre"""
    if value is None or value == '':
        return None
    
    value_str = str(value).strip()
    
    if not value_str or value_str == '*':
        return None
    
    value_str = re.sub(r'[^\d,.\-]', '', value_str)
    
    if not value_str:
        return None
    
    value_str = value_str.replace(',', '.')
    
    try:
        return float(value_str)
    except ValueError:
        return None


# =====================================================
# DÉTECTION AUTOMATIQUE DU FOURNISSEUR
# =====================================================

def detect_supplier(pdf_path):
    """
    Détecte automatiquement le type de fournisseur
    
    Returns:
        str: 'GDV', 'RICHARDSON', ou 'UNKNOWN'
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Lire le texte de la première page
            first_page_text = pdf.pages[0].extract_text()
            
            if not first_page_text:
                return 'UNKNOWN'
            
            text_upper = first_page_text.upper()
            
            # Détection GDV
            if 'LE DISTRIBUTEUR COURANTS FAIBLES' in first_page_text:
                return 'GDV'
            if 'GDV' in text_upper and 'COURANTS FAIBLES' in text_upper:
                return 'GDV'
            
            # Détection Richardson
            if 'RICHARDSON' in text_upper:
                return 'RICHARDSON'
            
            return 'UNKNOWN'
    
    except Exception as e:
        print(f"Erreur lors de la détection: {e}")
        return 'UNKNOWN'


# =====================================================
# PARSER GDV (existant)
# =====================================================

def extract_gdv(pdf_path):
    """Extrait les données d'une facture GDV"""
    
    def find_header_indices(row):
        indices = {}
        
        if not row:
            return indices
        
        for idx, cell in enumerate(row):
            if not cell:
                continue
            
            cell_lower = str(cell).lower().strip()
            
            if 'référence' in cell_lower or cell_lower == 'reference':
                indices['reference'] = idx
            elif 'désignation' in cell_lower or 'designation' in cell_lower:
                indices['designation'] = idx
            elif 'qté' in cell_lower or 'quantité' in cell_lower:
                indices['quantite'] = idx
            elif 'prix tarif' in cell_lower:
                indices['prix_tarif'] = idx
            elif 'remise' in cell_lower:
                indices['remise'] = idx
            elif 'p.u' in cell_lower:
                indices['pu_ht'] = idx
            elif 'montant ht' in cell_lower or 'montant' in cell_lower:
                indices['montant_ht'] = idx
        
        return indices
    
    def has_article_data(row):
        if not row or len(row) < 4:
            return False
        
        numeric_count = sum(1 for cell in row if cell and clean_number(cell) is not None)
        return numeric_count >= 2
    
    def is_header_row(row):
        if not row:
            return False
        
        row_text = ' '.join([str(cell).lower() for cell in row if cell])
        keywords = ['référence', 'designation', 'quantité', 'prix', 'montant']
        
        return any(keyword in row_text for keyword in keywords)
    
    invoice_data = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                tables = page.extract_tables()
                
                if not tables:
                    continue
                
                for table_num, table in enumerate(tables, 1):
                    if not table or len(table) < 2:
                        continue
                    
                    header_indices = {}
                    
                    for row in table:
                        if not row:
                            continue
                        
                        if not header_indices and is_header_row(row):
                            header_indices = find_header_indices(row)
                            continue
                        
                        if header_indices and has_article_data(row):
                            reference = row[header_indices.get('reference', 0)] if header_indices.get('reference') is not None else ''
                            designation = row[header_indices.get('designation', 2)] if header_indices.get('designation') is not None else ''
                            quantite = clean_number(row[header_indices.get('quantite', 7)]) if header_indices.get('quantite') is not None else None
                            prix_tarif = clean_number(row[header_indices.get('prix_tarif', 8)]) if header_indices.get('prix_tarif') is not None else None
                            montant_ht = clean_number(row[header_indices.get('montant_ht', 11)]) if header_indices.get('montant_ht') is not None else None
                            
                            if (designation or reference) and quantite is not None and montant_ht is not None:
                                invoice_data.append({
                                    'Fournisseur': 'GDV',
                                    'Fichier': Path(pdf_path).name,
                                    'Page': page_num,
                                    'Référence': str(reference).strip() if reference else '',
                                    'Désignation': str(designation).strip() if designation else '',
                                    'Quantité': quantite,
                                    'Prix tarif': prix_tarif,
                                    'Montant HT': montant_ht
                                })
    
    except Exception as e:
        print(f"Erreur GDV lors du traitement de {pdf_path}: {e}")
    
    return invoice_data


# =====================================================
# PARSER RICHARDSON (nouveau)
# =====================================================

def extract_richardson(pdf_path):
    """Extrait les données d'une facture Richardson"""
    invoice_data = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                
                if not text:
                    continue
                
                # Richardson a un format spécial : tout est dans le texte brut
                lines = text.split('\n')
                
                for i, line in enumerate(lines):
                    # Ignorer les lignes trop courtes ou spéciales
                    if len(line) < 20:
                        continue
                    
                    # Chercher les lignes avec pattern de quantité et montant
                    # Format: DESIGNATION ... U ... ... ...72,17 2 ...144,34 CODE
                    match = re.search(r'([\w\s\-/\.]+?)\s+U\s+\.+\s+\.+\s+([\d,\.]+)\s+(\d+)\s+\.+([\d,\.]+)\s+(\w+)', line)
                    
                    if match:
                        designation = match.group(1).strip()
                        prix_unitaire = clean_number(match.group(2))
                        quantite = clean_number(match.group(3))
                        montant = clean_number(match.group(4))
                        code = match.group(5).strip()
                        
                        # Filtrer ECOPARTICIPATION et autres lignes non-articles
                        if 'ECOPARTICIPATION' not in designation.upper() and \
                           'FRAIS DE PORT' not in designation.upper() and \
                           quantite and montant and montant > 1:  # Montant > 1€ pour éviter les écoparticipations
                            
                            invoice_data.append({
                                'Fournisseur': 'RICHARDSON',
                                'Fichier': Path(pdf_path).name,
                                'Page': page_num,
                                'Référence': code,
                                'Désignation': designation,
                                'Quantité': quantite,
                                'Prix tarif': prix_unitaire,
                                'Montant HT': montant
                            })
    
    except Exception as e:
        print(f"Erreur Richardson lors du traitement de {pdf_path}: {e}")
    
    return invoice_data


# =====================================================
# EXTRACTION UNIFIÉE
# =====================================================

def extract_invoice_data(pdf_path):
    """
    Extrait les données d'une facture (tous fournisseurs)
    Détecte automatiquement le type
    """
    supplier = detect_supplier(pdf_path)
    
    print(f"  Type détecté: {supplier}")
    
    if supplier == 'GDV':
        return extract_gdv(pdf_path)
    elif supplier == 'RICHARDSON':
        return extract_richardson(pdf_path)
    else:
        print(f"  ⚠️  Fournisseur non reconnu, tentative avec parser GDV...")
        return extract_gdv(pdf_path)


def process_invoices(pdf_files, output_file='factures_extraites.xlsx'):
    """Traite plusieurs factures et exporte vers Excel"""
    all_data = []
    
    print(f"Traitement de {len(pdf_files)} fichier(s)...\n")
    
    for pdf_file in pdf_files:
        print(f"Traitement de: {pdf_file}")
        data = extract_invoice_data(pdf_file)
        
        if data:
            all_data.extend(data)
            print(f"  → {len(data)} ligne(s) extraite(s)\n")
        else:
            print(f"  → Aucune donnée extraite\n")
    
    if not all_data:
        print("Aucune donnée extraite des factures.")
        return
    
    df = pd.DataFrame(all_data)
    df = df.sort_values(['Fournisseur', 'Fichier', 'Page'])
    
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"✓ Données exportées vers: {output_file}")
    print(f"  Total: {len(all_data)} ligne(s) extraite(s)")
    print(f"\nRésumé par fournisseur:")
    summary_supplier = df.groupby('Fournisseur').size()
    for fournisseur, count in summary_supplier.items():
        print(f"  - {fournisseur}: {count} ligne(s)")
    
    print(f"\nRésumé par fichier:")
    summary = df.groupby(['Fournisseur', 'Fichier']).size()
    for (fournisseur, fichier), count in summary.items():
        print(f"  - [{fournisseur}] {fichier}: {count} ligne(s)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_invoices_v3.py <fichier1.pdf> [fichier2.pdf] ...")
        sys.exit(1)
    
    pdf_files = sys.argv[1:]
    
    valid_files = []
    for pdf_file in pdf_files:
        if Path(pdf_file).exists():
            valid_files.append(pdf_file)
        else:
            print(f"Attention: {pdf_file} n'existe pas")
    
    if not valid_files:
        print("Aucun fichier PDF valide trouvé.")
        sys.exit(1)
    
    process_invoices(valid_files)


if __name__ == "__main__":
    main()
