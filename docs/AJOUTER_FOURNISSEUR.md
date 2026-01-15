# 📘 Guide : Ajouter un nouveau fournisseur

## 🎯 Vue d'ensemble

Ce guide vous explique comment ajouter un parser pour un nouveau fournisseur.

## 📋 Étapes

### 1. Analyser la facture

Utilisez ce script pour comprendre la structure :

```python
import pdfplumber

pdf_path = "facture_nouveau_fournisseur.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    
    # Extraire le texte
    text = page.extract_text()
    print("=== TEXTE BRUT ===")
    print(text[:1500])
    
    # Chercher les tableaux
    tables = page.extract_tables()
    print(f"\n=== TABLEAUX: {len(tables)} ===")
    
    if tables:
        for i, table in enumerate(tables, 1):
            print(f"\nTableau {i}:")
            for row in table[:5]:
                print(row)
```

### 2. Créer le fichier parser

Créez `src/parsers/nom_fournisseur.py` :

```python
"""
Parser pour les factures NOM_FOURNISSEUR
"""
import pdfplumber
import re
from pathlib import Path
from .base import BaseInvoiceParser
from ..utils import clean_number


class NomFournisseurParser(BaseInvoiceParser):
    """Parser pour les factures NOM_FOURNISSEUR"""
    
    def __init__(self):
        super().__init__()
        self.supplier_name = "NOM_FOURNISSEUR"
    
    def can_parse(self, text_content):
        """
        Détecte si c'est une facture de ce fournisseur
        
        Cherchez un mot-clé unique présent dans toutes les factures
        de ce fournisseur (nom, logo, numéro SIRET, etc.)
        """
        return 'MOT_CLE_UNIQUE' in text_content.upper()
    
    def extract(self, pdf_path):
        """Extrait les données de la facture"""
        invoice_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    
                    # OPTION A : Si la facture a des tableaux structurés
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            # Analyser chaque ligne du tableau
                            for row in table:
                                # Extraire les données...
                                pass
                    
                    # OPTION B : Si la facture est en texte pur
                    text = page.extract_text()
                    if text:
                        lines = text.split('\n')
                        for line in lines:
                            # Utiliser regex pour extraire...
                            match = re.search(r'VOTRE_PATTERN', line)
                            if match:
                                # Extraire les données...
                                pass
                    
                    # Ajouter l'article extrait
                    if condition:  # Si données valides
                        invoice_data.append({
                            'Fournisseur': self.supplier_name,
                            'Fichier': Path(pdf_path).name,
                            'Page': page_num,
                            'Référence': reference,
                            'Désignation': designation,
                            'Quantité': quantite,
                            'Montant HT': montant_ht,
                            # Autres colonnes spécifiques...
                        })
        
        except Exception as e:
            print(f"Erreur {self.supplier_name}: {e}")
        
        return invoice_data
```

### 3. Enregistrer le parser

Modifiez `src/parsers/__init__.py` :

```python
from .nom_fournisseur import NomFournisseurParser

ALL_PARSERS = [
    GDVParser(),
    RichardsonParser(),
    RexelParser(),
    LynelecParser(),
    NomFournisseurParser(),  # ← Ajoutez ici
]
```

### 4. Tester

```bash
python extract_invoices.py facture_test.pdf
```

## 🔍 Exemples de patterns

### Format tableau (comme GDV)

```python
# Chercher l'en-tête du tableau
for row in table:
    row_text = ' '.join([str(cell).lower() for cell in row if cell])
    if 'référence' in row_text and 'montant' in row_text:
        # C'est l'en-tête
        header_indices = self._find_header_indices(row)
```

### Format texte avec regex (comme Richardson/Rexel)

```python
# Pattern exemple : "REF123 DESIGNATION 10 €100.00"
match = re.search(r'([A-Z0-9]+)\s+(.+?)\s+(\d+)\s+€([\d,\.]+)', line)
if match:
    reference = match.group(1)
    designation = match.group(2)
    quantite = clean_number(match.group(3))
    montant = clean_number(match.group(4))
```

### Format sur plusieurs lignes (comme Lynelec)

```python
# Ligne 1 : "100 REF12345"
# Ligne 2 : "DESIGNATION 5 Km 50,00 250,00"

match_ref = re.match(r'^(\d+)\s+([A-Z0-9]+)', lines[i])
if match_ref and i + 1 < len(lines):
    reference = match_ref.group(2)
    next_line = lines[i + 1]
    # Extraire données de next_line...
```

## 💡 Conseils

### Détection robuste

Utilisez plusieurs mots-clés pour être sûr :

```python
def can_parse(self, text_content):
    text_upper = text_content.upper()
    return 'FOURNISSEUR' in text_upper and 'SIRET_UNIQUE' in text_upper
```

### Filtrer les lignes parasites

```python
# Ignorer les sous-totaux, titres, etc.
if 'SOUS-TOTAL' in designation.upper():
    continue
if not quantite or quantite == 0:
    continue
if montant < 1:  # Ignorer les montants trop petits
    continue
```

### Gérer les variations

```python
# Quantités avec unités
quantite_str = "5 Km" ou "10 L" ou "3 PCE"
quantite = clean_number(quantite_str.replace('Km', '').replace('L', '').replace('PCE', ''))
```

## 🧪 Tests

Testez avec plusieurs factures du même fournisseur pour vérifier :

✅ Détection correcte du fournisseur
✅ Extraction de tous les articles
✅ Pas de lignes parasites (sous-totaux, en-têtes)
✅ Nombres correctement extraits (format français/anglais)
✅ Gestion des factures multi-pages

## 🆘 Besoin d'aide ?

1. **Analysez d'abord** la structure avec le script d'analyse
2. **Identifiez** le pattern (tableau, texte, multi-lignes)
3. **Inspirez-vous** d'un parser similaire existant
4. **Testez** avec plusieurs factures
5. **Demandez de l'aide** si bloqué !

## 📊 Structure des données retournées

Format minimum requis :

```python
{
    'Fournisseur': str,      # Obligatoire
    'Fichier': str,          # Obligatoire
    'Page': int,             # Obligatoire
    'Référence': str,        # Recommandé
    'Désignation': str,      # Recommandé
    'Quantité': float,       # Obligatoire
    'Montant HT': float,     # Obligatoire
    # Colonnes supplémentaires selon le fournisseur
}
```

Colonnes facultatives courantes :
- `Prix tarif`
- `Prix net unitaire`
- `Remise %`
- `Prix base`
- `TVA %`

---

**Prêt à ajouter vos 7 autres fournisseurs !** 🚀
