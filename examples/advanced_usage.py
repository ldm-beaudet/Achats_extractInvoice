#!/usr/bin/env python3
"""
Exemple d'utilisation avancée de l'extracteur de factures

Cet exemple montre comment :
1. Traiter des factures d'un dossier spécifique
2. Filtrer par date
3. Générer un rapport avec statistiques
4. Exporter dans plusieurs formats
"""

from pathlib import Path
from datetime import datetime
import pandas as pd
from src.extract_invoices import extract_invoice_data


def extract_monthly_invoices(invoice_dir, month=None, year=None):
    """
    Extrait toutes les factures d'un mois donné
    
    Args:
        invoice_dir: Dossier contenant les factures
        month: Mois (1-12), par défaut le mois actuel
        year: Année (YYYY), par défaut l'année actuelle
    """
    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year
    
    invoice_dir = Path(invoice_dir)
    all_data = []
    
    # Chercher tous les PDFs
    pdf_files = list(invoice_dir.glob("*.pdf"))
    print(f"Trouvé {len(pdf_files)} fichier(s) PDF dans {invoice_dir}")
    
    # Extraire les données
    for pdf_file in pdf_files:
        print(f"Traitement de {pdf_file.name}...")
        data = extract_invoice_data(str(pdf_file))
        
        if data:
            all_data.extend(data)
            print(f"  → {len(data)} article(s) extrait(s)")
    
    if not all_data:
        print("Aucune donnée extraite.")
        return None
    
    # Créer un DataFrame
    df = pd.DataFrame(all_data)
    
    # Ajouter des métadonnées
    df['Date_extraction'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df['Mois'] = month
    df['Année'] = year
    
    return df


def generate_statistics(df):
    """
    Génère des statistiques sur les factures extraites
    """
    print("\n" + "="*60)
    print("STATISTIQUES DES FACTURES")
    print("="*60)
    
    # Nombre total d'articles
    print(f"\nTotal articles : {len(df)}")
    
    # Nombre de factures
    n_invoices = df['Fichier'].nunique()
    print(f"Nombre de factures : {n_invoices}")
    
    # Total HT
    total_ht = df['Montant HT'].sum()
    print(f"Total HT : {total_ht:,.2f} €")
    
    # Moyenne par article
    avg_article = df['Montant HT'].mean()
    print(f"Montant moyen par article : {avg_article:,.2f} €")
    
    # Par facture
    print(f"\nRépartition par facture :")
    summary = df.groupby('Fichier').agg({
        'Montant HT': ['count', 'sum', 'mean']
    }).round(2)
    print(summary)
    
    # Top 5 articles les plus chers
    print(f"\nTop 5 articles les plus chers :")
    top5 = df.nlargest(5, 'Montant HT')[['Désignation', 'Montant HT']]
    for idx, row in top5.iterrows():
        print(f"  - {row['Désignation'][:50]:50s} : {row['Montant HT']:>10.2f} €")
    
    # Articles par quantité
    print(f"\nQuantité totale commandée : {df['Quantité'].sum():,.0f}")
    
    return summary


def export_multiple_formats(df, base_name='factures'):
    """
    Exporte les données dans plusieurs formats
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Excel
    excel_file = f"{base_name}_{timestamp}.xlsx"
    df.to_excel(excel_file, index=False, engine='openpyxl')
    print(f"\n✓ Excel exporté : {excel_file}")
    
    # CSV
    csv_file = f"{base_name}_{timestamp}.csv"
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"✓ CSV exporté : {csv_file}")
    
    # JSON
    json_file = f"{base_name}_{timestamp}.json"
    df.to_json(json_file, orient='records', force_ascii=False, indent=2)
    print(f"✓ JSON exporté : {json_file}")
    
    return excel_file, csv_file, json_file


def create_summary_report(df, output_file='rapport_factures.xlsx'):
    """
    Crée un rapport Excel avec plusieurs onglets
    """
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Onglet 1 : Données brutes
        df.to_excel(writer, sheet_name='Données', index=False)
        
        # Onglet 2 : Résumé par facture
        summary_by_invoice = df.groupby('Fichier').agg({
            'Montant HT': ['count', 'sum', 'mean', 'min', 'max']
        }).round(2)
        summary_by_invoice.columns = ['Nb_articles', 'Total_HT', 'Moyen_HT', 'Min_HT', 'Max_HT']
        summary_by_invoice.to_excel(writer, sheet_name='Résumé_factures')
        
        # Onglet 3 : Top articles
        top_articles = df.nlargest(20, 'Montant HT')[
            ['Fichier', 'Référence', 'Désignation', 'Quantité', 'Montant HT']
        ]
        top_articles.to_excel(writer, sheet_name='Top_20_articles', index=False)
        
        # Onglet 4 : Statistiques globales
        stats_data = {
            'Métrique': [
                'Nombre total de factures',
                'Nombre total d\'articles',
                'Montant total HT',
                'Montant moyen par facture',
                'Montant moyen par article',
                'Quantité totale'
            ],
            'Valeur': [
                df['Fichier'].nunique(),
                len(df),
                f"{df['Montant HT'].sum():,.2f} €",
                f"{df.groupby('Fichier')['Montant HT'].sum().mean():,.2f} €",
                f"{df['Montant HT'].mean():,.2f} €",
                f"{df['Quantité'].sum():,.0f}"
            ]
        }
        stats_df = pd.DataFrame(stats_data)
        stats_df.to_excel(writer, sheet_name='Statistiques', index=False)
    
    print(f"\n✓ Rapport détaillé créé : {output_file}")


def main():
    """
    Exemple d'utilisation complète
    """
    print("="*60)
    print("EXTRACTEUR DE FACTURES - EXEMPLE AVANCÉ")
    print("="*60)
    
    # Configuration
    INVOICE_DIR = Path("mes_factures")  # Adaptez ce chemin
    
    # Vérifier que le dossier existe
    if not INVOICE_DIR.exists():
        print(f"\n⚠️  Le dossier {INVOICE_DIR} n'existe pas.")
        print("Créez-le et placez-y vos factures PDF, ou modifiez le chemin dans le script.")
        return
    
    # Extraction
    print(f"\n1. Extraction des factures de {INVOICE_DIR}...")
    df = extract_monthly_invoices(INVOICE_DIR)
    
    if df is None:
        return
    
    # Statistiques
    print("\n2. Génération des statistiques...")
    generate_statistics(df)
    
    # Export multi-formats
    print("\n3. Export dans plusieurs formats...")
    export_multiple_formats(df, base_name='factures_mensuelles')
    
    # Rapport détaillé
    print("\n4. Création du rapport détaillé...")
    create_summary_report(df, output_file='rapport_detaille.xlsx')
    
    print("\n" + "="*60)
    print("✓ TRAITEMENT TERMINÉ")
    print("="*60)
    print("\nFichiers générés :")
    print("  - factures_mensuelles_[timestamp].xlsx (données brutes)")
    print("  - factures_mensuelles_[timestamp].csv")
    print("  - factures_mensuelles_[timestamp].json")
    print("  - rapport_detaille.xlsx (avec statistiques)")


if __name__ == "__main__":
    main()
