#!/usr/bin/env python3
"""
Extracteur de factures multi-fournisseurs - Architecture modulaire
Version 6.0 - Supporte actuellement 4 fournisseurs, extensible à 11+
"""

import sys
from pathlib import Path
import pandas as pd

# Importer les parsers
from src.parsers import ALL_PARSERS
from src.utils import extract_first_page_text


def detect_supplier(pdf_path):
    """
    Détecte automatiquement quel parser utiliser
    
    Args:
        pdf_path: Chemin vers le PDF
        
    Returns:
        BaseInvoiceParser ou None: Parser approprié ou None si non reconnu
    """
    text = extract_first_page_text(pdf_path)
    
    if not text:
        return None
    
    # Tester chaque parser
    for parser in ALL_PARSERS:
        if parser.can_parse(text):
            return parser
    
    return None


def extract_invoice_data(pdf_path):
    """
    Extrait les données d'une facture
    
    Args:
        pdf_path: Chemin vers le PDF
        
    Returns:
        list: Liste de dictionnaires avec les données extraites
    """
    parser = detect_supplier(pdf_path)
    
    if parser:
        print(f"  Type détecté: {parser.get_supplier_name()}")
        return parser.extract(pdf_path)
    else:
        print(f"  ⚠️  Fournisseur non reconnu")
        return []


def process_invoices(pdf_files, output_file='factures_extraites.xlsx'):
    """
    Traite plusieurs factures et exporte vers Excel
    
    Args:
        pdf_files: Liste des chemins vers les PDFs
        output_file: Nom du fichier Excel de sortie
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
        print("❌ Aucune donnée extraite des factures.")
        return
    
    # Créer DataFrame et trier
    df = pd.DataFrame(all_data)
    df = df.sort_values(['Fournisseur', 'Fichier', 'Page'])
    
    # Exporter vers Excel
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    # Afficher résumé
    print(f"✓ Données exportées vers: {output_file}")
    print(f"  Total: {len(all_data)} ligne(s) extraite(s)")
    
    print(f"\n📊 Résumé par fournisseur:")
    summary_supplier = df.groupby('Fournisseur').size()
    for fournisseur, count in summary_supplier.items():
        print(f"  - {fournisseur}: {count} ligne(s)")
    
    print(f"\n📋 Résumé par fichier:")
    summary = df.groupby(['Fournisseur', 'Fichier']).size()
    for (fournisseur, fichier), count in summary.items():
        print(f"  - [{fournisseur}] {fichier}: {count} ligne(s)")


def main():
    """Point d'entrée principal"""
    if len(sys.argv) < 2:
        print("Usage: python extract_invoices.py <fichier1.pdf> [fichier2.pdf] ...")
        print("\nExemple:")
        print("  python extract_invoices.py Factures/*.pdf")
        print("  python extract_invoices.py facture1.pdf facture2.pdf")
        sys.exit(1)
    
    pdf_files = sys.argv[1:]
    
    # Valider les fichiers
    valid_files = []
    for pdf_file in pdf_files:
        if Path(pdf_file).exists():
            valid_files.append(pdf_file)
        else:
            print(f"⚠️  Attention: {pdf_file} n'existe pas")
    
    if not valid_files:
        print("❌ Aucun fichier PDF valide trouvé.")
        sys.exit(1)
    
    # Traiter les factures
    process_invoices(valid_files)


if __name__ == "__main__":
    main()
