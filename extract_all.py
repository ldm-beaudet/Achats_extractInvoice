#!/usr/bin/env python3
"""
Script pour extraire automatiquement toutes les factures du dossier Factures/
"""
import glob
import os
from src.extract_invoices import process_invoices

# Dossier contenant les factures
FACTURES_DIR = "Factures"

# Chercher tous les PDFs
pdf_files = glob.glob(f"{FACTURES_DIR}/*.pdf")

if not pdf_files:
    print(f"❌ Aucun PDF trouvé dans {FACTURES_DIR}/")
    print(f"Dossier actuel : {os.getcwd()}")
    print(f"\nVérifiez que vous avez bien des fichiers .pdf dans le dossier {FACTURES_DIR}/")
else:
    print(f"✓ Trouvé {len(pdf_files)} fichier(s) PDF")
    print(f"\nDémarrage de l'extraction...\n")
    
    # Traiter toutes les factures
    process_invoices(pdf_files, output_file='factures_extraites.xlsx')
    
    print(f"\n{'='*60}")
    print("✓ EXTRACTION TERMINÉE")
    print(f"{'='*60}")
    print(f"Fichier généré : factures_extraites.xlsx")
    print(f"Vous pouvez maintenant l'ouvrir dans Excel !")