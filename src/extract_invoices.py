#!/usr/bin/env python3
"""
Script d'extraction de données de factures PDF - Version améliorée
Spécialement adapté pour les factures avec mise en page complexe
"""

import pdfplumber
import pandas as pd
import re
from pathlib import Path
import sys


def clean_number(value):
    """
    Nettoie et convertit une valeur en nombre
    """
    if value is None or value == '':
        return None
    
    value_str = str(value).strip()
    
    if not value_str or value_str == '*':
        return None
    
    # Supprimer les espaces et caractères non numériques sauf , . et -
    value_str = re.sub(r'[^\d,.\-]', '', value_str)
    
    if not value_str:
        return None
    
    # Remplacer la virgule par un point pour la conversion
    value_str = value_str.replace(',', '.')
    
    try:
        return float(value_str)
    except ValueError:
        return None


def is_header_row(row):
    """
    Vérifie si une ligne est une ligne d'en-tête
    """
    if not row:
        return False
    
    row_text = ' '.join([str(cell).lower() for cell in row if cell])
    header_keywords = ['référence', 'designation', 'désignation', 'quantité', 'qté', 
                       'prix', 'montant', 'tarif', 'remise', 'p.u']
    
    return any(keyword in row_text for keyword in header_keywords)


def has_article_data(row):
    """
    Vérifie si une ligne contient des données d'article significatives
    """
    if not row or len(row) < 4:
        return False
    
    # Vérifier s'il y a au moins une quantité ou un montant numérique
    numeric_count = 0
    for cell in row:
        if cell and clean_number(cell) is not None:
            numeric_count += 1
    
    # Il faut au moins 2 valeurs numériques (qté + prix ou prix + montant)
    return numeric_count >= 2


def extract_article_from_row(row, header_indices):
    """
    Extrait les données d'un article d'une ligne
    """
    reference = ''
    designation = ''
    quantite = None
    prix_tarif = None
    remise = None
    pu_ht = None
    montant_ht = None
    
    # Extraire selon les indices trouvés dans l'en-tête
    if header_indices.get('reference') is not None:
        idx = header_indices['reference']
        if idx < len(row) and row[idx]:
            reference = str(row[idx]).strip()
    
    if header_indices.get('designation') is not None:
        idx = header_indices['designation']
        if idx < len(row) and row[idx]:
            designation = str(row[idx]).strip()
    
    if header_indices.get('quantite') is not None:
        idx = header_indices['quantite']
        if idx < len(row) and row[idx]:
            quantite = clean_number(row[idx])
    
    if header_indices.get('prix_tarif') is not None:
        idx = header_indices['prix_tarif']
        if idx < len(row) and row[idx]:
            prix_tarif = clean_number(row[idx])
    
    if header_indices.get('remise') is not None:
        idx = header_indices['remise']
        if idx < len(row) and row[idx]:
            remise = clean_number(row[idx])
    
    if header_indices.get('pu_ht') is not None:
        idx = header_indices['pu_ht']
        if idx < len(row) and row[idx]:
            pu_ht = clean_number(row[idx])
    
    if header_indices.get('montant_ht') is not None:
        idx = header_indices['montant_ht']
        if idx < len(row) and row[idx]:
            montant_ht = clean_number(row[idx])
    
    return {
        'reference': reference,
        'designation': designation,
        'quantite': quantite,
        'prix_tarif': prix_tarif,
        'remise': remise,
        'pu_ht': pu_ht,
        'montant_ht': montant_ht
    }


def find_header_indices(row):
    """
    Identifie les indices des colonnes dans l'en-tête
    """
    indices = {}
    
    for idx, cell in enumerate(row):
        if not cell:
            continue
        
        cell_lower = str(cell).lower().strip()
        
        if 'référence' in cell_lower or cell_lower == 'reference':
            indices['reference'] = idx
        elif 'désignation' in cell_lower or 'designation' in cell_lower or 'description' in cell_lower:
            indices['designation'] = idx
        elif 'qté' in cell_lower or 'quantité' in cell_lower or 'quantite' in cell_lower:
            indices['quantite'] = idx
        elif 'prix tarif' in cell_lower or 'prix_tarif' in cell_lower:
            indices['prix_tarif'] = idx
        elif 'remise' in cell_lower:
            indices['remise'] = idx
        elif 'p.u' in cell_lower or 'p.u.' in cell_lower or 'pu h.t' in cell_lower:
            indices['pu_ht'] = idx
        elif 'montant ht' in cell_lower or 'montant' in cell_lower:
            indices['montant_ht'] = idx
    
    return indices


def extract_invoice_data(pdf_path):
    """
    Extrait les données d'une facture PDF
    """
    invoice_data = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                tables = page.extract_tables()
                
                if not tables:
                    print(f"Page {page_num}: Aucun tableau détecté")
                    continue
                
                # Chercher le tableau principal avec les articles
                for table_num, table in enumerate(tables, 1):
                    if not table or len(table) < 2:
                        continue
                    
                    header_indices = {}
                    article_lines = []
                    
                    # Parcourir le tableau pour trouver l'en-tête et les lignes d'articles
                    for row_idx, row in enumerate(table):
                        if not row:
                            continue
                        
                        # Chercher la ligne d'en-tête
                        if not header_indices and is_header_row(row):
                            header_indices = find_header_indices(row)
                            print(f"  En-tête trouvé à la ligne {row_idx}: {header_indices}")
                            continue
                        
                        # Si on a trouvé l'en-tête, chercher les lignes de données
                        if header_indices and has_article_data(row):
                            article_lines.append(row)
                    
                    # Extraire les données des lignes d'articles
                    if article_lines and header_indices:
                        print(f"  Trouvé {len(article_lines)} ligne(s) d'article(s)")
                        
                        for row in article_lines:
                            article = extract_article_from_row(row, header_indices)
                            
                            # Ne garder que les lignes avec au moins une quantité ET un montant
                            # Cela évite de capturer les lignes de description ou de numéro BL
                            if (article['designation'] or article['reference']) and \
                               article['quantite'] is not None and \
                               article['montant_ht'] is not None:
                                invoice_data.append({
                                    'Fichier': Path(pdf_path).name,
                                    'Page': page_num,
                                    'Référence': article['reference'],
                                    'Désignation': article['designation'],
                                    'Quantité': article['quantite'],
                                    'Prix tarif': article['prix_tarif'],
                                    'Remise': article['remise'],
                                    'P.U H.T': article['pu_ht'],
                                    'Montant HT': article['montant_ht']
                                })
    
    except Exception as e:
        print(f"Erreur lors du traitement de {pdf_path}: {e}")
        import traceback
        traceback.print_exc()
        return []
    
    return invoice_data


def process_invoices(pdf_files, output_file='factures_extraites.xlsx'):
    """
    Traite plusieurs factures et exporte vers Excel
    """
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
    
    # Créer un DataFrame et exporter vers Excel
    df = pd.DataFrame(all_data)
    
    # Trier par fichier et page
    df = df.sort_values(['Fichier', 'Page'])
    
    # Exporter vers Excel
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"✓ Données exportées vers: {output_file}")
    print(f"  Total: {len(all_data)} ligne(s) extraite(s)")
    print(f"\nRésumé par fichier:")
    summary = df.groupby('Fichier').size()
    for fichier, count in summary.items():
        print(f"  - {fichier}: {count} ligne(s)")
    
    # Afficher un aperçu des données
    print(f"\nAperçu des données extraites:")
    print(df.to_string(index=False))


def main():
    """Point d'entrée principal du script"""
    
    if len(sys.argv) < 2:
        print("Usage: python extract_invoices_v2.py <fichier1.pdf> [fichier2.pdf] ...")
        print("\nOu pour traiter tous les PDFs d'un dossier:")
        print("python extract_invoices_v2.py *.pdf")
        sys.exit(1)
    
    # Récupérer les fichiers PDF
    pdf_files = sys.argv[1:]
    
    # Vérifier que les fichiers existent
    valid_files = []
    for pdf_file in pdf_files:
        if Path(pdf_file).exists():
            valid_files.append(pdf_file)
        else:
            print(f"Attention: {pdf_file} n'existe pas")
    
    if not valid_files:
        print("Aucun fichier PDF valide trouvé.")
        sys.exit(1)
    
    # Traiter les factures
    process_invoices(valid_files)


if __name__ == "__main__":
    main()
