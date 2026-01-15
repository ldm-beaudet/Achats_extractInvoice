"""
Script pour identifier et analyser les factures problématiques
Fonctionne pour TOUS les fournisseurs (pas seulement Nollet)
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
                            return parser, None
    except Exception as e:
        return None, str(e)
    return None, None

def main():
    print("="*80)
    print("  ANALYSE DES FACTURES PROBLÉMATIQUES")
    print("="*80)
    
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
    
    print(f"\n📄 Analyse de {len(pdf_files)} fichier(s)...")
    print(f"⏱️  Début : {datetime.now().strftime('%H:%M:%S')}")
    print("-"*80)
    
    # Catégories de problèmes
    non_reconnus = []      # Aucun parser ne reconnaît
    erreurs_lecture = []   # Erreur lors de la lecture du PDF
    aucune_donnee = []     # Parser reconnaît mais extrait 0 ligne
    succes = {}            # Fichiers OK par fournisseur
    
    # Analyse
    for i, pdf_path in enumerate(pdf_files, 1):
        if i % 100 == 0:
            pct = (i / len(pdf_files)) * 100
            print(f"  [{i}/{len(pdf_files)}] ({pct:.1f}%)")
        
        # Détecter le fournisseur
        parser, error = detect_supplier(pdf_path)
        
        if error:
            # Erreur de lecture
            erreurs_lecture.append({
                'fichier': pdf_path.name,
                'erreur': error[:100]  # Limiter à 100 caractères
            })
            continue
        
        if not parser:
            # Non reconnu
            non_reconnus.append(pdf_path.name)
            continue
        
        # Tenter l'extraction
        try:
            data = parser.extract(str(pdf_path))
            
            if data:
                # Succès
                supplier = parser.supplier_name
                if supplier not in succes:
                    succes[supplier] = []
                succes[supplier].append({
                    'fichier': pdf_path.name,
                    'lignes': len(data)
                })
            else:
                # Aucune donnée extraite
                aucune_donnee.append({
                    'fichier': pdf_path.name,
                    'fournisseur': parser.supplier_name
                })
        except Exception as e:
            erreurs_lecture.append({
                'fichier': pdf_path.name,
                'erreur': f"Erreur extraction: {str(e)[:80]}"
            })
    
    # Affichage des résultats
    print("\n" + "="*80)
    print("  RÉSULTATS DE L'ANALYSE")
    print("="*80)
    
    total_problemes = len(non_reconnus) + len(erreurs_lecture) + len(aucune_donnee)
    total_succes = sum(len(files) for files in succes.values())
    
    print(f"\n📊 RÉSUMÉ GLOBAL :")
    print(f"   • Fichiers analysés      : {len(pdf_files)}")
    print(f"   • Fichiers OK            : {total_succes} ({total_succes/len(pdf_files)*100:.1f}%)")
    print(f"   • Fichiers problématiques: {total_problemes} ({total_problemes/len(pdf_files)*100:.1f}%)")
    
    # Détail par fournisseur
    if succes:
        print(f"\n✅ FICHIERS TRAITÉS AVEC SUCCÈS PAR FOURNISSEUR :")
        for supplier in sorted(succes.keys()):
            files = succes[supplier]
            total_lignes = sum(f['lignes'] for f in files)
            print(f"   • {supplier:15s} : {len(files):4d} fichiers, {total_lignes:6d} lignes")
    
    # Non reconnus
    if non_reconnus:
        print(f"\n⚠️  FICHIERS NON RECONNUS ({len(non_reconnus)}) :")
        print("   (Aucun parser ne correspond)")
        for i, fichier in enumerate(non_reconnus[:20], 1):  # Limiter à 20
            print(f"   {i:2d}. {fichier}")
        if len(non_reconnus) > 20:
            print(f"   ... et {len(non_reconnus) - 20} autres")
        
        # Exporter la liste complète
        with open("fichiers_non_reconnus.txt", "w", encoding="utf-8") as f:
            f.write("FICHIERS NON RECONNUS\n")
            f.write("=" * 80 + "\n\n")
            for fichier in sorted(non_reconnus):
                f.write(f"{fichier}\n")
        print(f"\n   📄 Liste complète exportée : fichiers_non_reconnus.txt")
    
    # Erreurs de lecture
    if erreurs_lecture:
        print(f"\n❌ ERREURS DE LECTURE ({len(erreurs_lecture)}) :")
        print("   (PDFs corrompus, protégés ou illisibles)")
        for i, info in enumerate(erreurs_lecture[:10], 1):  # Limiter à 10
            print(f"   {i:2d}. {info['fichier']}")
            print(f"       → {info['erreur']}")
        if len(erreurs_lecture) > 10:
            print(f"   ... et {len(erreurs_lecture) - 10} autres")
        
        # Exporter la liste complète
        with open("fichiers_erreurs.txt", "w", encoding="utf-8") as f:
            f.write("FICHIERS AVEC ERREURS\n")
            f.write("=" * 80 + "\n\n")
            for info in erreurs_lecture:
                f.write(f"{info['fichier']}\n")
                f.write(f"  Erreur: {info['erreur']}\n\n")
        print(f"\n   📄 Liste complète exportée : fichiers_erreurs.txt")
    
    # Aucune donnée
    if aucune_donnee:
        print(f"\n⚠️  FICHIERS SANS DONNÉES EXTRAITES ({len(aucune_donnee)}) :")
        print("   (Parser reconnaît mais n'extrait rien)")
        
        # Grouper par fournisseur
        par_fournisseur = {}
        for info in aucune_donnee:
            supplier = info['fournisseur']
            if supplier not in par_fournisseur:
                par_fournisseur[supplier] = []
            par_fournisseur[supplier].append(info['fichier'])
        
        for supplier in sorted(par_fournisseur.keys()):
            fichiers = par_fournisseur[supplier]
            print(f"\n   {supplier} ({len(fichiers)} fichiers) :")
            for i, fichier in enumerate(fichiers[:10], 1):  # Limiter à 10 par fournisseur
                print(f"      {i:2d}. {fichier}")
            if len(fichiers) > 10:
                print(f"      ... et {len(fichiers) - 10} autres")
        
        # Exporter la liste complète
        with open("fichiers_sans_donnees.txt", "w", encoding="utf-8") as f:
            f.write("FICHIERS SANS DONNÉES EXTRAITES\n")
            f.write("=" * 80 + "\n\n")
            for supplier in sorted(par_fournisseur.keys()):
                f.write(f"\n{supplier}:\n")
                f.write("-" * 40 + "\n")
                for fichier in sorted(par_fournisseur[supplier]):
                    f.write(f"  {fichier}\n")
        print(f"\n   📄 Liste complète exportée : fichiers_sans_donnees.txt")
    
    # Créer un Excel récapitulatif
    if total_problemes > 0:
        print(f"\n📊 Création du rapport Excel...")
        
        data_excel = []
        
        # Non reconnus
        for fichier in non_reconnus:
            data_excel.append({
                'Fichier': fichier,
                'Catégorie': 'Non reconnu',
                'Fournisseur': '',
                'Détail': 'Aucun parser ne correspond'
            })
        
        # Erreurs
        for info in erreurs_lecture:
            data_excel.append({
                'Fichier': info['fichier'],
                'Catégorie': 'Erreur lecture',
                'Fournisseur': '',
                'Détail': info['erreur']
            })
        
        # Sans données
        for info in aucune_donnee:
            data_excel.append({
                'Fichier': info['fichier'],
                'Catégorie': 'Sans données',
                'Fournisseur': info['fournisseur'],
                'Détail': 'Parser reconnaît mais 0 ligne extraite'
            })
        
        df = pd.DataFrame(data_excel)
        df = df.sort_values(['Catégorie', 'Fournisseur', 'Fichier'])
        df.to_excel("rapport_fichiers_problematiques.xlsx", index=False)
        
        print(f"   ✅ Rapport Excel créé : rapport_fichiers_problematiques.xlsx")
    
    print("\n" + "="*80)
    print("  ANALYSE TERMINÉE")
    print("="*80)
    
    if total_problemes == 0:
        print("\n🎉 Aucun fichier problématique détecté !")
    else:
        print(f"\n📋 Fichiers créés :")
        if non_reconnus:
            print("   • fichiers_non_reconnus.txt")
        if erreurs_lecture:
            print("   • fichiers_erreurs.txt")
        if aucune_donnee:
            print("   • fichiers_sans_donnees.txt")
        if total_problemes > 0:
            print("   • rapport_fichiers_problematiques.xlsx")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analyse interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale : {e}")
        import traceback
        traceback.print_exc()