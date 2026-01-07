# 💡 Exemples d'utilisation

Ce dossier contient des exemples pratiques pour utiliser l'extracteur de factures PDF.

## 📋 Liste des exemples

### 1. create_demo_invoice.py
Crée une facture PDF de démonstration pour tester l'extracteur.

**Utilisation** :
```bash
python examples/create_demo_invoice.py
```

**Ce qu'il fait** :
- Génère un fichier `facture_demo.pdf`
- Contient 6 articles avec quantités et prix
- Structure identique aux vraies factures

**Quand l'utiliser** :
- Pour tester l'installation
- Pour développer sans avoir de vraies factures
- Pour créer des tests

### 2. advanced_usage.py
Exemple complet montrant des fonctionnalités avancées.

**Utilisation** :
```bash
python examples/advanced_usage.py
```

**Ce qu'il fait** :
- Extrait toutes les factures d'un dossier
- Génère des statistiques détaillées
- Exporte dans plusieurs formats (Excel, CSV, JSON)
- Crée un rapport avec plusieurs onglets

**Quand l'utiliser** :
- Pour automatiser le traitement mensuel
- Pour générer des rapports comptables
- Comme base pour vos propres scripts

## 🎯 Cas d'usage courants

### Traitement mensuel automatique

Créez un script `process_monthly.py` :

```python
from pathlib import Path
from datetime import datetime
from src.extract_invoices import process_invoices

# Dossier des factures
factures_dir = Path("~/Documents/Factures").expanduser()
mois = datetime.now().strftime("%Y-%m")

# Trouver et traiter
pdfs = list(factures_dir.glob(f"*{mois}*.pdf"))
process_invoices([str(p) for p in pdfs], f"factures_{mois}.xlsx")
```

### Filtrer par fournisseur

```python
from pathlib import Path
from src.extract_invoices import process_invoices

# Toutes les factures GDV
factures_gdv = list(Path("factures").glob("F*.pdf"))
process_invoices([str(f) for f in factures_gdv], "factures_gdv.xlsx")
```

### Comparer deux périodes

```python
import pandas as pd

# Charger deux exports
q1 = pd.read_excel("factures_Q1.xlsx")
q2 = pd.read_excel("factures_Q2.xlsx")

# Comparer
print(f"Q1: {q1['Montant HT'].sum():,.2f} €")
print(f"Q2: {q2['Montant HT'].sum():,.2f} €")
print(f"Évolution: {((q2['Montant HT'].sum() / q1['Montant HT'].sum()) - 1) * 100:.1f}%")
```

### Exporter pour comptabilité

```python
from src.extract_invoices import extract_invoice_data
import pandas as pd

# Extraire avec format comptable
all_data = []
for pdf in factures:
    data = extract_invoice_data(pdf)
    all_data.extend(data)

df = pd.DataFrame(all_data)

# Colonnes pour logiciel comptable
df_compta = df[['Fichier', 'Référence', 'Désignation', 'Montant HT']]
df_compta['TVA'] = df_compta['Montant HT'] * 0.20
df_compta['TTC'] = df_compta['Montant HT'] * 1.20

df_compta.to_csv('export_compta.csv', index=False, sep=';')
```

## 🔧 Personnalisation

### Adapter pour vos factures

Si vos factures ont un format différent, créez un exemple personnalisé :

```python
# examples/custom_extraction.py
from src.extract_invoices import extract_invoice_data, find_header_indices

# Ajouter vos propres mots-clés
def custom_find_header_indices(row):
    indices = find_header_indices(row)
    
    # Ajouter détection spécifique
    for idx, cell in enumerate(row):
        if 'votre_colonne_spéciale' in str(cell).lower():
            indices['custom'] = idx
    
    return indices
```

### Ajouter des calculs

```python
# examples/with_calculations.py
import pandas as pd
from src.extract_invoices import process_invoices

# Extraction normale
process_invoices(['facture.pdf'], 'temp.xlsx')

# Charger et enrichir
df = pd.read_excel('temp.xlsx')

# Ajouter TVA
df['TVA'] = df['Montant HT'] * 0.20
df['TTC'] = df['Montant HT'] + df['TVA']

# Catégoriser
def categorize(designation):
    if 'CENTRALE' in str(designation).upper():
        return 'Matériel'
    elif 'CPU' in str(designation).upper():
        return 'Électronique'
    else:
        return 'Autre'

df['Catégorie'] = df['Désignation'].apply(categorize)

# Sauvegarder
df.to_excel('factures_enrichies.xlsx', index=False)
```

## 📊 Visualisation des données

### Créer des graphiques

```python
# examples/visualization.py
import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
df = pd.read_excel('factures_extraites.xlsx')

# Graphique 1 : Montants par facture
df.groupby('Fichier')['Montant HT'].sum().plot(kind='bar')
plt.title('Montant HT par facture')
plt.ylabel('Montant (€)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('montants_par_facture.png')
plt.close()

# Graphique 2 : Distribution des prix
df['Montant HT'].hist(bins=20)
plt.title('Distribution des montants')
plt.xlabel('Montant (€)')
plt.ylabel('Fréquence')
plt.savefig('distribution_montants.png')
```

## 🤖 Automatisation

### Script Bash (Linux/macOS)

```bash
#!/bin/bash
# examples/auto_extract.sh

# Traiter toutes les nouvelles factures
cd ~/Documents
python ~/extracteur-factures-pdf/src/extract_invoices.py Factures/*.pdf

# Déplacer le résultat
mv factures_extraites.xlsx Comptabilite/factures_$(date +%Y-%m).xlsx

echo "✓ Factures extraites et archivées"
```

### Task Scheduler (Windows)

```batch
REM examples/auto_extract.bat
@echo off

cd C:\Users\VotreNom\Documents
python C:\extracteur-factures-pdf\src\extract_invoices.py Factures\*.pdf

move factures_extraites.xlsx Comptabilite\factures_%date:~-7,4%-%date:~-10,2%.xlsx

echo ✓ Factures extraites et archivées
```

## 🎓 Pour aller plus loin

### Intégration avec d'autres outils

```python
# examples/integration.py

# 1. Envoyer par email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_report(excel_file):
    # ... code d'envoi email ...
    pass

# 2. Uploader sur Google Drive
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(file_path):
    # ... code Google Drive API ...
    pass

# 3. Insérer dans base de données
import sqlite3

def insert_to_db(df):
    conn = sqlite3.connect('factures.db')
    df.to_sql('articles', conn, if_exists='append', index=False)
    conn.close()
```

## 📚 Ressources

- [Documentation pandas](https://pandas.pydata.org/docs/)
- [Documentation pdfplumber](https://github.com/jsvine/pdfplumber)
- [Tutoriel Excel avec Python](https://realpython.com/openpyxl-excel-spreadsheets-python/)

## ❓ Questions

Des questions sur les exemples ? Ouvrez une [issue](https://github.com/votre-username/extracteur-factures-pdf/issues) !

---

**Astuce** : Copiez ces exemples et adaptez-les à vos besoins spécifiques !
