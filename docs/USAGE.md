# 📖 Guide d'utilisation

Guide complet pour utiliser l'extracteur de factures PDF.

## Table des matières

1. [Utilisation basique](#utilisation-basique)
2. [Options avancées](#options-avancées)
3. [Utilisation en Python](#utilisation-en-python)
4. [Formats de factures](#formats-de-factures)
5. [Personnalisation](#personnalisation)
6. [Bonnes pratiques](#bonnes-pratiques)

## Utilisation basique

### Extraire une seule facture

```bash
python src/extract_invoices.py ma_facture.pdf
```

**Résultat** : Crée un fichier `factures_extraites.xlsx` dans le dossier courant.

### Extraire plusieurs factures

```bash
python src/extract_invoices.py facture1.pdf facture2.pdf facture3.pdf
```

Toutes les factures seront consolidées dans un seul fichier Excel.

### Extraire toutes les factures d'un dossier

```bash
# Linux/macOS
python src/extract_invoices.py /chemin/vers/factures/*.pdf

# Windows
python src/extract_invoices.py C:\Factures\*.pdf
```

### Exemple avec chemin complet

```bash
cd extracteur-factures-pdf
python src/extract_invoices.py ~/Documents/Factures/janvier_2025/*.pdf
```

## Options avancées

### Spécifier un nom de fichier de sortie

Modifiez le script ou utilisez-le en tant que module Python (voir plus bas).

### Traiter des factures de différents dossiers

```bash
python src/extract_invoices.py \
  /dossier1/*.pdf \
  /dossier2/*.pdf \
  /dossier3/facture_specifique.pdf
```

## Utilisation en Python

Vous pouvez utiliser l'extracteur comme une bibliothèque Python :

### Import basique

```python
from src.extract_invoices import process_invoices

# Liste de fichiers PDF
factures = [
    'facture_janvier.pdf',
    'facture_fevrier.pdf',
    'facture_mars.pdf'
]

# Extraction avec nom personnalisé
process_invoices(factures, output_file='factures_Q1_2025.xlsx')
```

### Exemple complet

```python
from pathlib import Path
from src.extract_invoices import process_invoices, extract_invoice_data

# Trouver tous les PDFs dans un dossier
dossier = Path('mes_factures')
pdf_files = list(dossier.glob('*.pdf'))

# Extraire les données
process_invoices([str(f) for f in pdf_files], output_file='resultat.xlsx')

# Ou extraire une seule facture pour inspecter les données
data = extract_invoice_data('ma_facture.pdf')
print(f"Trouvé {len(data)} articles")
for article in data:
    print(f"- {article['Désignation']}: {article['Montant HT']}€")
```

### Script automatisé

Créez un script pour traiter automatiquement vos factures :

```python
#!/usr/bin/env python3
"""
Script pour traiter toutes les nouvelles factures chaque mois
"""
from pathlib import Path
from datetime import datetime
from src.extract_invoices import process_invoices

# Configuration
DOSSIER_FACTURES = Path("~/Documents/Factures").expanduser()
DOSSIER_SORTIE = Path("~/Documents/Comptabilite").expanduser()

# Date actuelle
mois_actuel = datetime.now().strftime("%Y-%m")

# Trouver les factures du mois
factures = list(DOSSIER_FACTURES.glob(f"*{mois_actuel}*.pdf"))

if factures:
    print(f"Traitement de {len(factures)} facture(s)...")
    
    # Nom du fichier de sortie
    output = DOSSIER_SORTIE / f"factures_{mois_actuel}.xlsx"
    
    # Extraction
    process_invoices([str(f) for f in factures], output_file=str(output))
    
    print(f"✓ Terminé ! Fichier créé : {output}")
else:
    print("Aucune facture trouvée pour ce mois.")
```

## Formats de factures

### Formats testés et supportés

✅ **Factures GDV** (Le Distributeur Courants Faibles)
- Structure avec tableaux standards
- Colonnes : Référence, Désignation, Qté, Prix tarif, Remise, P.U H.T, Montant HT

✅ **Factures avec tableaux standards**
- En-têtes clairs
- Une ligne = un article

✅ **Factures multi-pages**
- Articles répartis sur plusieurs pages

### Colonnes reconnues automatiquement

Le script détecte automatiquement ces noms de colonnes (et leurs variantes) :

| Type | Variantes reconnues |
|------|---------------------|
| **Référence** | référence, reference, ref, code article |
| **Désignation** | désignation, designation, description, libellé, libelle, article, produit |
| **Quantité** | quantité, quantite, qté, qte, qty, nombre |
| **Prix tarif** | prix tarif, prix catalogue, tarif |
| **Remise** | remise, discount, réduction |
| **P.U H.T** | p.u h.t, p.u., prix unitaire, pu ht |
| **Montant HT** | montant ht, montant, total, prix total |

### Formats de nombres supportés

Le script gère automatiquement :
- Format français : `1 234,56` ou `1.234,56`
- Format anglais : `1,234.56`
- Avec symboles : `1 234,56 €` ou `$1,234.56`

## Personnalisation

### Ajouter de nouveaux mots-clés

Éditez le fichier `src/extract_invoices.py` :

```python
def find_header_indices(row):
    # ...
    for idx, cell in enumerate(row):
        cell_lower = str(cell).lower().strip()
        
        # Ajoutez vos propres mots-clés ici
        if 'votre_mot_clé' in cell_lower:
            indices['votre_colonne'] = idx
```

### Modifier les critères de filtrage

Par défaut, le script ne garde que les lignes avec quantité ET montant.

Pour modifier ce comportement :

```python
# Dans extract_invoice_data()
if (article['designation'] or article['reference']) and \
   article['quantite'] is not None and \
   article['montant_ht'] is not None:
    # Modifiez cette condition selon vos besoins
```

### Changer le format de sortie

Actuellement Excel (.xlsx). Pour CSV :

```python
import pandas as pd

# Au lieu de to_excel()
df.to_csv('factures.csv', index=False, encoding='utf-8-sig')
```

## Bonnes pratiques

### Organisation des fichiers

```
📁 Mes Documents/
  📁 Factures/
    📁 2025/
      📁 Janvier/
        📄 F2504861.pdf
        📄 F2504866.pdf
      📁 Fevrier/
        📄 F2505123.pdf
  📁 Comptabilite/
    📄 factures_2025-01.xlsx
    📄 factures_2025-02.xlsx
```

### Nommage des factures

Utilisez un format cohérent pour vos factures :
- `FYYYYMMDD.pdf` (exemple : F20250131.pdf)
- `Facture_FOURNISSEUR_DATE.pdf`
- `F[Numéro].pdf` (comme vos factures actuelles)

### Workflow recommandé

1. **Collecte** : Placez toutes vos factures dans un dossier
2. **Extraction** : Lancez le script sur tout le dossier
3. **Vérification** : Ouvrez l'Excel et vérifiez les totaux
4. **Archivage** : Déplacez les factures traitées dans un dossier "Traité"

### Script bash automatique (Linux/macOS)

```bash
#!/bin/bash
# extract_monthly.sh

FACTURES_DIR="$HOME/Documents/Factures"
OUTPUT_DIR="$HOME/Documents/Comptabilite"
MOIS=$(date +%Y-%m)

python src/extract_invoices.py "$FACTURES_DIR"/*.pdf

# Renommer le fichier de sortie
mv factures_extraites.xlsx "$OUTPUT_DIR/factures_$MOIS.xlsx"

echo "✓ Factures du mois extraites dans $OUTPUT_DIR/factures_$MOIS.xlsx"
```

### Script batch automatique (Windows)

```batch
@echo off
REM extract_monthly.bat

set FACTURES_DIR=C:\Users\VotreNom\Documents\Factures
set OUTPUT_DIR=C:\Users\VotreNom\Documents\Comptabilite
set MOIS=%date:~-7,4%-%date:~-10,2%

python src\extract_invoices.py "%FACTURES_DIR%\*.pdf"

move factures_extraites.xlsx "%OUTPUT_DIR%\factures_%MOIS%.xlsx"

echo ✓ Factures du mois extraites dans %OUTPUT_DIR%\factures_%MOIS%.xlsx
pause
```

## Vérification des résultats

### Toujours vérifier

1. **Le nombre de lignes** : Correspond-il au nombre d'articles ?
2. **Les totaux** : Faites une somme dans Excel et comparez
3. **Les données manquantes** : Y a-t-il des cellules vides ?

### Formule Excel pour vérifier les totaux

Dans Excel, ajoutez une cellule :
```excel
=SOMME(I:I)  // Colonne Montant HT
```

Comparez avec le total de la facture.

## Cas d'usage avancés

### Traiter uniquement les factures d'un fournisseur

```bash
python src/extract_invoices.py factures/GDV*.pdf
```

### Exclure certaines factures

```python
from pathlib import Path

# Tous les PDFs sauf ceux commençant par "DRAFT"
factures = [
    str(f) for f in Path('factures').glob('*.pdf')
    if not f.name.startswith('DRAFT')
]

process_invoices(factures)
```

### Fusionner plusieurs extractions

```python
import pandas as pd

# Charger plusieurs fichiers Excel
df1 = pd.read_excel('factures_janvier.xlsx')
df2 = pd.read_excel('factures_fevrier.xlsx')
df3 = pd.read_excel('factures_mars.xlsx')

# Fusionner
df_total = pd.concat([df1, df2, df3], ignore_index=True)

# Sauvegarder
df_total.to_excel('factures_Q1_2025.xlsx', index=False)
```

## Problèmes courants

Voir [TROUBLESHOOTING.md](TROUBLESHOOTING.md) pour une liste complète.

## Exemples supplémentaires

Consultez le dossier [examples/](../examples/) pour plus d'exemples de code.

---

**Questions ?** Consultez la [FAQ](TROUBLESHOOTING.md#faq) ou ouvrez une [issue](https://github.com/votre-username/extracteur-factures-pdf/issues).
