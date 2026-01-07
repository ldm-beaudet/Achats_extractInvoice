# 📄 Extracteur de Factures PDF

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Un outil Python simple et efficace pour extraire automatiquement les données des factures PDF (libellés, quantités, montants) et les exporter vers Excel.

![Demo](https://img.shields.io/badge/demo-working-success)

## ✨ Fonctionnalités

- ✅ Extraction automatique des articles de factures
- ✅ Détection intelligente des colonnes (référence, désignation, quantité, prix, montant)
- ✅ Gestion des formats de nombres français (1 234,56 €) et anglais (1,234.56)
- ✅ Traitement par lot de plusieurs factures
- ✅ Export direct vers Excel (.xlsx)
- ✅ Support des mises en page complexes
- ✅ Filtrage automatique des lignes parasites

## 📋 Table des matières

- [Installation](#-installation)
- [Utilisation rapide](#-utilisation-rapide)
- [Documentation](#-documentation)
- [Exemples](#-exemples)
- [Structure du projet](#-structure-du-projet)
- [Contribution](#-contribution)
- [Licence](#-licence)

## 🚀 Installation

### Prérequis

- Python 3.6 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
# Cloner le repository
git clone https://github.com/votre-username/extracteur-factures-pdf.git
cd extracteur-factures-pdf

# Installer les dépendances
pip install -r requirements.txt
```

### Installation en tant que package (optionnel)

```bash
pip install -e .
```

## ⚡ Utilisation rapide

### Extraire une facture

```bash
python src/extract_invoices.py chemin/vers/facture.pdf
```

### Extraire plusieurs factures

```bash
python src/extract_invoices.py facture1.pdf facture2.pdf facture3.pdf
```

### Extraire toutes les factures d'un dossier

```bash
python src/extract_invoices.py /chemin/vers/dossier/*.pdf
```

### Résultat

Un fichier `factures_extraites.xlsx` est généré automatiquement avec :

| Fichier | Page | Référence | Désignation | Quantité | Prix tarif | P.U H.T | Montant HT |
|---------|------|-----------|-------------|----------|------------|---------|------------|
| F2504861.pdf | 1 | FER-CVE | CENTRALE VIGIK ÉVOLUÉE | 1.0 | 295.93 | 295.93 | 295.93 |

## 📚 Documentation

- [Guide d'installation détaillé](docs/INSTALLATION.md)
- [Guide d'utilisation complet](docs/USAGE.md)
- [Résolution de problèmes](docs/TROUBLESHOOTING.md)
- [API Reference](docs/API.md) (pour développeurs)

## 💡 Exemples

### Créer une facture de test

```bash
python examples/create_demo_invoice.py
```

### Exemple de code Python

```python
from src.extract_invoices import process_invoices

# Traiter des factures
pdf_files = ['facture1.pdf', 'facture2.pdf']
process_invoices(pdf_files, output_file='mes_factures.xlsx')
```

Voir plus d'exemples dans le dossier [examples/](examples/)

## 📁 Structure du projet

```
extracteur-factures-pdf/
├── README.md                    # Ce fichier
├── LICENSE                      # Licence MIT
├── requirements.txt             # Dépendances Python
├── setup.py                     # Configuration du package
├── .gitignore                   # Fichiers à ignorer
│
├── src/                         # Code source
│   ├── __init__.py
│   └── extract_invoices.py      # Script principal
│
├── examples/                    # Exemples et démos
│   ├── demo_invoice.pdf
│   └── create_demo_invoice.py
│
├── tests/                       # Tests unitaires
│   └── test_extraction.py
│
├── docs/                        # Documentation
│   ├── INSTALLATION.md
│   ├── USAGE.md
│   ├── TROUBLESHOOTING.md
│   └── API.md
│
└── output/                      # Résultats d'extraction
    └── .gitkeep
```

## 🧪 Tests

```bash
# Exécuter les tests
python -m pytest tests/

# Avec couverture de code
python -m pytest --cov=src tests/
```

## 🛠️ Technologies utilisées

- **pdfplumber** - Extraction de texte et tableaux des PDFs
- **pandas** - Manipulation et analyse de données
- **openpyxl** - Création de fichiers Excel
- **reportlab** - Génération de PDFs de démonstration

## 📊 Formats de factures supportés

Le script a été testé et validé sur :
- ✅ Factures GDV (Le Distributeur Courants Faibles)
- ✅ Factures avec tableaux standards
- ✅ Factures avec mises en page complexes
- ✅ Factures multi-lignes

**Note** : Les PDFs doivent contenir du texte (pas des images scannées). Pour les factures scannées, un OCR est nécessaire.

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. Créez votre branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une **Pull Request**

Voir [CONTRIBUTING.md](docs/CONTRIBUTING.md) pour plus de détails.

## 📝 Roadmap

- [ ] Interface graphique (GUI)
- [ ] Support de l'OCR pour factures scannées
- [ ] Export vers d'autres formats (CSV, JSON, SQL)
- [ ] Extraction des informations d'en-tête (n° facture, date, client)
- [ ] API REST
- [ ] Support multi-langue
- [ ] Reconnaissance automatique du format de facture

## 🐛 Bugs connus

- Avertissements `Cannot set gray non-stroke color` (bénins, peuvent être ignorés)
- Les tableaux très complexes peuvent nécessiter des ajustements

Voir [Issues](https://github.com/votre-username/extracteur-factures-pdf/issues) pour la liste complète.

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**Votre Nom**
- GitHub: [@votre-username](https://github.com/votre-username)
- Email: votre.email@example.com

## 🙏 Remerciements

- La communauté Python
- Les développeurs de pdfplumber
- Tous les contributeurs du projet

## 📞 Support

Si vous rencontrez des problèmes :
1. Consultez la [documentation](docs/)
2. Vérifiez les [issues existantes](https://github.com/votre-username/extracteur-factures-pdf/issues)
3. Ouvrez une [nouvelle issue](https://github.com/votre-username/extracteur-factures-pdf/issues/new)

---

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile sur GitHub !
