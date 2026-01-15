"""
Script helper pour extraire toutes les factures du dossier Factures/
Version optimisée pour gros volumes (1000+ fichiers)
"""
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le dossier courant au path
sys.path.insert(0, str(Path(__file__).parent))

from src.parsers import ALL_PARSERS
import pandas as pd

def detect_supplier(pdf_path):
    """Détecte le fournisseur d'une facture"""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            if pdf.pages:
                text = pdf.pages[0].extract_text()
                if text:
                    for parser in ALL_PARSERS:
                        if parser.can_parse(text):
                            return parser
    except Exception as e:
        return None
    return None

def main():
    print("="*70)
    print("  EXTRACTEUR DE FACTURES - TRAITEMENT PAR LOT")
    print("="*70)
    
    # Dossier contenant les factures
    factures_dir = Path("Factures")
    
    if not factures_dir.exists():
        print(f"\n❌ Le dossier {factures_dir} n'existe pas")
        return
    
    # Trouver tous les PDFs
    pdf_files = sorted(factures_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"\n❌ Aucun fichier PDF trouvé dans {factures_dir}/")
        return
    
    total_files = len(pdf_files)
    print(f"\n📄 {total_files} fichier(s) PDF détecté(s)")
    print(f"⏱️  Début du traitement : {datetime.now().strftime('%H:%M:%S')}")
    print("-"*70)
    
    all_data = []
    stats_by_supplier = {}
    stats_by_file = {}
    processed = 0
    errors = 0
    unrecognized = 0
    
    # Traitement avec progression
    for i, pdf_path in enumerate(pdf_files, 1):
        # Afficher progression tous les 10 fichiers
        if i % 10 == 0 or i == 1:
            pct = (i / total_files) * 100
            print(f"\n[{i}/{total_files}] ({pct:.1f}%) - {pdf_path.name}")
        
        # Détecter le fournisseur
        parser = detect_supplier(pdf_path)
        
        if not parser:
            unrecognized += 1
            continue
        
        # Extraire les données
        try:
            data = parser.extract(str(pdf_path))
            
            if data:
                all_data.extend(data)
                processed += 1
                
                # Stats
                supplier = parser.supplier_name
                stats_by_supplier[supplier] = stats_by_supplier.get(supplier, 0) + len(data)
                
                if supplier not in stats_by_file:
                    stats_by_file[supplier] = []
                stats_by_file[supplier].append({
                    'file': pdf_path.name,
                    'count': len(data)
                })
            else:
                errors += 1
        except Exception as e:
            errors += 1
    
    print("\n" + "="*70)
    print("  TRAITEMENT TERMINÉ")
    print("="*70)
    print(f"⏱️  Fin : {datetime.now().strftime('%H:%M:%S')}")
    
    # Exporter les résultats
    if all_data:
        df = pd.DataFrame(all_data)
        output_file = "factures_extraites.xlsx"
        
        print(f"\n📊 Exportation vers {output_file}...")
        df.to_excel(output_file, index=False)
        
        print(f"\n✅ RÉSULTATS :")
        print(f"   • Total lignes extraites : {len(all_data)}")
        print(f"   • Fichiers traités avec succès : {processed}/{total_files}")
        print(f"   • Fichiers non reconnus : {unrecognized}")
        if errors > 0:
            print(f"   • Erreurs : {errors}")
        
        print(f"\n📊 RÉPARTITION PAR FOURNISSEUR :")
        for supplier in sorted(stats_by_supplier.keys()):
            count = stats_by_supplier[supplier]
            files = len(stats_by_file[supplier])
            print(f"   • {supplier:15s} : {count:5d} lignes ({files} fichiers)")
        
        # Top 10 des fichiers par fournisseur
        print(f"\n📋 TOP 10 DES FICHIERS PAR FOURNISSEUR :")
        for supplier in sorted(stats_by_file.keys()):
            files = stats_by_file[supplier]
            top_files = sorted(files, key=lambda x: x['count'], reverse=True)[:3]
            print(f"\n   {supplier} :")
            for f in top_files:
                print(f"      - {f['file']}: {f['count']} ligne(s)")
        
        print(f"\n✅ Fichier Excel généré : {output_file}")
    else:
        print("\n❌ Aucune donnée extraite")
        if unrecognized > 0:
            print(f"   {unrecognized} fichiers non reconnus")
        if errors > 0:
            print(f"   {errors} erreurs rencontrées")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Traitement interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale : {e}")
        import traceback
        traceback.print_exc()