# 🔧 Guide de résolution de problèmes

Solutions aux problèmes courants rencontrés avec l'extracteur de factures PDF.

## Table des matières

1. [Aucune donnée extraite](#aucune-donnée-extraite)
2. [Données incomplètes](#données-incomplètes)
3. [Erreurs d'exécution](#erreurs-dexécution)
4. [Problèmes de format](#problèmes-de-format)
5. [Performance](#performance)
6. [FAQ](#faq)

## Aucune donnée extraite

### Symptôme
```
Traitement de: ma_facture.pdf
  → Aucune donnée extraite
```

### Causes possibles

#### 1. PDF scanné (image au lieu de texte)

**Diagnostic** :
```bash
python -c "import pdfplumber; pdf = pdfplumber.open('facture.pdf'); print(pdf.pages[0].extract_text())"
```

Si aucun texte n'apparaît, votre PDF est une image.

**Solution** : Utilisez un OCR (Reconnaissance Optique de Caractères) :

```python
# Installation : pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('facture_scannee.pdf')
for i, image in enumerate(images):
    text = pytesseract.image_to_string(image, lang='fra')
    print(f"Page {i+1}:\n{text}")
```

#### 2. Structure de tableau non reconnue

**Diagnostic** : Utilisez le script de debug :

```bash
python debug_pdf.py
```

**Solution** : Ajustez les mots-clés de détection dans `find_header_indices()`.

#### 3. Pas de tableau dans le PDF

**Solution** : Le PDF ne contient peut-être pas de tableau structuré. Essayez l'extraction de texte brut.

## Données incomplètes

### Symptôme
Certaines colonnes sont vides (NaN) dans le fichier Excel.

### Causes et solutions

#### 1. Colonne non détectée

**Vérification** :
```python
# Regardez les en-têtes détectés dans les logs
En-tête trouvé : {'reference': 0, 'designation': 2, ...}
```

**Solution** : Ajoutez des variantes de noms dans `find_header_indices()` :

```python
elif 'votre_variante' in cell_lower or 'autre_nom' in cell_lower:
    indices['quantite'] = idx
```

#### 2. Format de nombre non reconnu

**Exemple** : `1'234.56` (format suisse) n'est pas reconnu.

**Solution** : Modifiez la fonction `clean_number()` :

```python
def clean_number(value):
    # Ajouter le support du format suisse
    value_str = str(value).strip()
    value_str = value_str.replace("'", "")  # Apostrophe
    # ... reste du code
```

#### 3. Ligne filtrée par erreur

Le script filtre les lignes sans quantité ET montant.

**Solution** : Assurez la condition de filtrage :

```python
# Au lieu de AND, utilisez OR pour être moins strict
if (article['designation'] or article['reference']) and \
   (article['quantite'] is not None or article['montant_ht'] is not None):
```

## Erreurs d'exécution

### "ModuleNotFoundError: No module named 'pdfplumber'"

**Cause** : Dépendances non installées.

**Solution** :
```bash
pip install -r requirements.txt
```

### "FileNotFoundError: [Errno 2] No such file or directory"

**Cause** : Chemin de fichier incorrect.

**Solutions** :
```bash
# Utiliser le chemin absolu
python src/extract_invoices.py /chemin/complet/vers/facture.pdf

# Ou se placer dans le bon dossier
cd /chemin/vers/factures
python /chemin/vers/extracteur-factures-pdf/src/extract_invoices.py *.pdf
```

### "PermissionError: [Errno 13] Permission denied"

**Cause** : Le fichier Excel est ouvert dans Excel.

**Solution** : Fermez le fichier Excel et réessayez.

### "Cannot set gray non-stroke color"

**Cause** : Problème mineur dans le PDF (bénin).

**Solution** : Ignorez ces avertissements, ils n'affectent pas l'extraction.

Pour les masquer :
```python
import warnings
warnings.filterwarnings('ignore')
```

### "UnicodeDecodeError"

**Cause** : Caractères spéciaux dans les noms de fichiers.

**Solution** : Renommez vos fichiers sans accents ni caractères spéciaux.

## Problèmes de format

### Montants incorrects

#### Symptôme
`1234,56` devient `123456.0`

**Cause** : Problème de conversion des virgules/points.

**Solution** : Vérifiez la fonction `clean_number()` :

```python
# Debug
def clean_number(value):
    print(f"Avant nettoyage: {value}")
    # ... code de nettoyage
    result = float(value_str)
    print(f"Après nettoyage: {result}")
    return result
```

### Texte coupé dans les cellules

**Cause** : Désignations longues tronquées.

**Solution Excel** : Ajustez la largeur des colonnes ou activez le retour à la ligne.

### Colonnes désordonnées

**Cause** : Ordre des colonnes dans le PDF différent.

**Solution** : Le script s'adapte automatiquement. Si problème, vérifiez les indices dans les logs.

## Performance

### Le script est lent

**Pour 100 factures :**
- Temps normal : ~2-3 minutes
- Temps lent : >10 minutes

**Solutions** :

1. **Traiter en lot** :
```python
# Au lieu de boucler sur process_invoices()
# Passez tous les fichiers en une seule fois
process_invoices(all_pdf_files)
```

2. **Utiliser plusieurs processus** (avancé) :
```python
from multiprocessing import Pool

def extract_one(pdf_file):
    return extract_invoice_data(pdf_file)

with Pool(4) as pool:  # 4 processus parallèles
    results = pool.map(extract_one, pdf_files)
```

### Fichier Excel volumineux

**Si >100 Mo** :

1. Séparez par période :
```python
# Un fichier par mois
process_invoices(factures_janvier, 'janvier.xlsx')
process_invoices(factures_fevrier, 'fevrier.xlsx')
```

2. Utilisez CSV au lieu d'Excel :
```python
df.to_csv('factures.csv', index=False)
```

## Débogage avancé

### Mode verbeux

Ajoutez des prints pour voir ce qui se passe :

```python
def extract_invoice_data(pdf_path):
    print(f"\n{'='*60}")
    print(f"Traitement de : {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Nombre de pages : {len(pdf.pages)}")
        
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"\n--- Page {page_num} ---")
            tables = page.extract_tables()
            print(f"Tableaux trouvés : {len(tables)}")
            
            for table_num, table in enumerate(tables, 1):
                print(f"\nTableau {table_num} - {len(table)} lignes")
                # ... reste du code
```

### Sauvegarder les données intermédiaires

```python
import json

# Sauvegarder les données extraites avant export Excel
with open('debug_data.json', 'w', encoding='utf-8') as f:
    json.dump(invoice_data, f, ensure_ascii=False, indent=2)
```

### Inspecter un tableau spécifique

```python
import pdfplumber

with pdfplumber.open('facture.pdf') as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables()
    
    # Afficher le 2ème tableau
    print("Tableau 2:")
    for i, row in enumerate(tables[1]):
        print(f"Ligne {i}: {row}")
```

## FAQ

### Q1 : Le script fonctionne-t-il sur Mac/Windows/Linux ?

**R** : Oui, il fonctionne sur les trois systèmes d'exploitation.

### Q2 : Puis-je traiter des factures en anglais ?

**R** : Oui, ajoutez simplement les mots-clés anglais :
```python
if 'quantity' in cell_lower or 'qty' in cell_lower:
    indices['quantite'] = idx
```

### Q3 : Le script peut-il extraire les logos ou images ?

**R** : Non, uniquement le texte et les données tabulaires. Pour les images, utilisez `pdf2image`.

### Q4 : Combien de factures puis-je traiter en une fois ?

**R** : Illimité en théorie. En pratique, 1000+ factures fonctionnent bien.

### Q5 : Puis-je extraire d'autres informations (date, numéro de facture) ?

**R** : Oui ! Ajoutez le code d'extraction dans `extract_invoice_data()` :

```python
# Extraire le numéro de facture
text = page.extract_text()
import re
numero = re.search(r'FACTURE\s*N°?\s*(\d+)', text)
if numero:
    invoice_data['numero_facture'] = numero.group(1)
```

### Q6 : Le fichier Excel est-il compatible avec Google Sheets ?

**R** : Oui, vous pouvez l'importer directement dans Google Sheets.

### Q7 : Puis-je automatiser l'extraction quotidiennement ?

**R** : Oui, avec un cron job (Linux/Mac) ou Task Scheduler (Windows) :

```bash
# Cron job quotidien à 9h
0 9 * * * cd /chemin/projet && python src/extract_invoices.py ~/factures/*.pdf
```

### Q8 : Les données sont-elles sécurisées ?

**R** : Oui, tout est traité localement. Aucune donnée n'est envoyée sur internet.

### Q9 : Puis-je modifier le script pour mes besoins ?

**R** : Absolument ! Le code est sous licence MIT, vous pouvez le modifier librement.

### Q10 : Comment contribuer au projet ?

**R** : Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.

## Obtenir de l'aide

Si votre problème n'est pas listé ici :

1. **Cherchez dans les issues GitHub** : [Issues](https://github.com/votre-username/extracteur-factures-pdf/issues)
2. **Ouvrez une nouvelle issue** avec :
   - Description du problème
   - Message d'erreur complet
   - Version de Python utilisée
   - Exemple de fichier PDF (si possible)
3. **Contactez-moi** : votre.email@example.com

## Ressources utiles

- [Documentation pdfplumber](https://github.com/jsvine/pdfplumber)
- [Documentation pandas](https://pandas.pydata.org/docs/)
- [Regex Python](https://docs.python.org/3/library/re.html)

---

**Conseil** : Gardez ce fichier à portée de main ! La plupart des problèmes ont une solution simple. 😊
