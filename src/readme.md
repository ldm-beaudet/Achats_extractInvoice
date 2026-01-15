# Extracteur de Factures PDF - Architecture Modulaire

Extraction automatique de données depuis factures PDF multi-fournisseurs.

## 🚀 Version actuelle : v7.0

**10 fournisseurs supportés** (91% de couverture) :
- GDV, Richardson, Rexel, Lynelec, Caparol
- Clareo, Nollet, Sonepar, BCL Decor, Point P

## 📦 Installation
```bash
pip install pdfplumber pandas openpyxl
```

## 🎯 Utilisation
```bash
# Une ou plusieurs factures
python extract_invoices.py facture1.pdf facture2.pdf

# Toutes les factures d'un dossier
python extract_invoices.py Factures/*.pdf
```

## 🏗️ Architecture

- **Script principal** : `extract_invoices.py` (~100 lignes)
- **Parsers** : Un fichier par fournisseur dans `src/parsers/`
- **Documentation** : Guide complet dans `docs/`

## ➕ Ajouter un nouveau fournisseur

Voir le guide détaillé : `docs/AJOUTER_FOURNISSEUR.md`

Temps estimé : **5-10 minutes par fournisseur**