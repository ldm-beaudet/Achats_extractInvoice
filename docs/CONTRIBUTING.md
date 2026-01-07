# 🤝 Guide de contribution

Merci de votre intérêt pour contribuer à l'extracteur de factures PDF ! Ce guide vous explique comment participer au projet.

## Table des matières

1. [Code de conduite](#code-de-conduite)
2. [Comment contribuer](#comment-contribuer)
3. [Processus de développement](#processus-de-développement)
4. [Standards de code](#standards-de-code)
5. [Tests](#tests)
6. [Documentation](#documentation)

## Code de conduite

### Nos valeurs

- **Respect** : Soyez respectueux envers tous les contributeurs
- **Bienveillance** : Aidez les débutants et partagez vos connaissances
- **Constructivité** : Les critiques doivent être constructives
- **Inclusivité** : Tout le monde est le bienvenu, quel que soit son niveau

### Comportements inacceptables

- Langage offensant ou discriminatoire
- Harcèlement sous toute forme
- Publication d'informations privées sans permission

## Comment contribuer

### 🐛 Signaler un bug

1. **Vérifiez** que le bug n'a pas déjà été signalé dans les [Issues](https://github.com/votre-username/extracteur-factures-pdf/issues)
2. **Créez une nouvelle issue** avec le template "Bug Report"
3. **Incluez** :
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu vs réel
   - Version de Python
   - Message d'erreur complet
   - Exemple de PDF (si possible)

### 💡 Proposer une fonctionnalité

1. **Vérifiez** que la fonctionnalité n'est pas déjà proposée
2. **Créez une issue** avec le template "Feature Request"
3. **Expliquez** :
   - Le problème que ça résoudrait
   - Comment vous imaginez l'implémentation
   - Des exemples d'utilisation

### 📝 Améliorer la documentation

La documentation est cruciale ! N'hésitez pas à :
- Corriger des fautes
- Clarifier des explications
- Ajouter des exemples
- Traduire dans d'autres langues

### 🔧 Contribuer du code

#### 1. Fork et clone

```bash
# Forker le projet sur GitHub, puis :
git clone https://github.com/votre-username/extracteur-factures-pdf.git
cd extracteur-factures-pdf
```

#### 2. Créer une branche

```bash
git checkout -b feature/ma-fonctionnalite
# ou
git checkout -b fix/mon-correctif
```

Noms de branches recommandés :
- `feature/nom-de-la-fonctionnalite`
- `fix/description-du-bug`
- `docs/amelioration-doc`
- `refactor/nom-du-refactoring`

#### 3. Installer en mode développement

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer avec dépendances de dev
pip install -e ".[dev]"
```

#### 4. Faire vos modifications

Suivez les [standards de code](#standards-de-code).

#### 5. Tester

```bash
# Exécuter les tests
pytest tests/

# Avec couverture
pytest --cov=src tests/
```

#### 6. Commiter

```bash
git add .
git commit -m "feat: description de la fonctionnalité"
```

**Convention de commit** (optionnel mais recommandé) :
- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `docs:` documentation
- `style:` formatage
- `refactor:` refactorisation
- `test:` ajout de tests
- `chore:` maintenance

#### 7. Pousser et créer une Pull Request

```bash
git push origin feature/ma-fonctionnalite
```

Puis sur GitHub, créez une Pull Request avec :
- Titre clair
- Description de ce qui a changé
- Référence aux issues concernées (#123)
- Screenshots si pertinent

## Processus de développement

### Structure du code

```
src/
├── __init__.py           # Exports publics
├── extract_invoices.py   # Logique principale
├── parsers.py            # (futur) Parseurs spécifiques
└── utils.py              # (futur) Fonctions utilitaires
```

### Workflow

1. **Issue** → Discussion sur la fonctionnalité/bug
2. **Development** → Code + Tests
3. **Pull Request** → Review du code
4. **Merge** → Intégration dans `main`
5. **Release** → Tag + changelog

### Revue de code

Toutes les PRs sont revues. Soyez patient et ouvert aux suggestions !

**Critères de validation** :
- ✅ Le code fonctionne
- ✅ Les tests passent
- ✅ La documentation est à jour
- ✅ Le style est cohérent
- ✅ Pas de régression

## Standards de code

### Style Python

Nous suivons [PEP 8](https://pep8.org/) avec quelques adaptations.

**Formatage automatique** :
```bash
# Installer black
pip install black

# Formater
black src/ tests/
```

**Linting** :
```bash
# Installer flake8
pip install flake8

# Vérifier
flake8 src/ tests/
```

### Conventions de nommage

```python
# Variables et fonctions : snake_case
ma_variable = 10
def ma_fonction():
    pass

# Classes : PascalCase
class MonParseur:
    pass

# Constantes : UPPER_SNAKE_CASE
MAX_RETRIES = 3
```

### Documentation

Toutes les fonctions publiques doivent avoir une docstring :

```python
def extract_invoice_data(pdf_path):
    """
    Extrait les données d'une facture PDF.
    
    Args:
        pdf_path (str): Chemin vers le fichier PDF
        
    Returns:
        list: Liste de dictionnaires contenant les articles
        
    Raises:
        FileNotFoundError: Si le PDF n'existe pas
        
    Example:
        >>> data = extract_invoice_data('facture.pdf')
        >>> print(len(data))
        5
    """
    # Code...
```

### Type hints (optionnel mais apprécié)

```python
from typing import List, Dict, Optional

def process_invoices(
    pdf_files: List[str], 
    output_file: str = 'factures.xlsx'
) -> None:
    """Process multiple invoices."""
    pass
```

## Tests

### Écrire des tests

```python
# tests/test_extraction.py
import pytest
from src.extract_invoices import clean_number

def test_clean_number_french():
    """Test conversion nombre français."""
    assert clean_number("1 234,56") == 1234.56
    assert clean_number("1.234,56") == 1234.56

def test_clean_number_english():
    """Test conversion nombre anglais."""
    assert clean_number("1,234.56") == 1234.56

def test_clean_number_invalid():
    """Test valeur invalide."""
    assert clean_number("abc") is None
    assert clean_number("") is None
```

### Lancer les tests

```bash
# Tous les tests
pytest

# Un fichier spécifique
pytest tests/test_extraction.py

# Une fonction spécifique
pytest tests/test_extraction.py::test_clean_number_french

# Avec verbosité
pytest -v

# Avec couverture
pytest --cov=src --cov-report=html
```

### Couverture de code

Visez >80% de couverture pour le nouveau code.

```bash
# Générer un rapport
pytest --cov=src --cov-report=html
# Ouvrir htmlcov/index.html dans un navigateur
```

## Documentation

### Mettre à jour la documentation

Si vous ajoutez/modifiez une fonctionnalité :

1. **README.md** : Mettre à jour si fonctionnalité majeure
2. **docs/USAGE.md** : Ajouter des exemples d'utilisation
3. **docs/API.md** : Documenter les nouvelles fonctions
4. **Docstrings** : Toujours à jour

### Ajouter des exemples

Les exemples sont dans `examples/`. Format :

```python
#!/usr/bin/env python3
"""
Titre de l'exemple
Description de ce qu'il fait
"""

# Code avec commentaires explicatifs
```

## Bonnes pratiques

### ✅ À faire

- ✅ Tester votre code sur plusieurs types de factures
- ✅ Ajouter des tests pour les nouvelles fonctionnalités
- ✅ Mettre à jour la documentation
- ✅ Faire des commits atomiques (une fonctionnalité = un commit)
- ✅ Écrire des messages de commit clairs
- ✅ Demander de l'aide si vous bloquez

### ❌ À éviter

- ❌ Commits énormes avec plein de changements
- ❌ Code non testé
- ❌ Documentation manquante
- ❌ Modifier des fichiers sans rapport avec votre issue
- ❌ Copier-coller du code sans attribution

## Ressources pour les débutants

### Première contribution ?

Super ! Voici des ressources utiles :

- [First Contributions](https://github.com/firstcontributions/first-contributions)
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

### Issues pour débutants

Cherchez les labels :
- `good first issue` : Parfait pour débuter
- `help wanted` : Besoin d'aide
- `documentation` : Améliorer la doc

### Questions ?

N'hésitez pas à poser des questions dans les issues ou discussions !

## Communauté

### Discussions

Utilisez [GitHub Discussions](https://github.com/votre-username/extracteur-factures-pdf/discussions) pour :
- Questions générales
- Idées de fonctionnalités
- Partager vos cas d'usage
- Demander de l'aide

### Contact

- **Email** : votre.email@example.com
- **Twitter** : @votre_handle
- **Discord** : (si vous en avez un)

## Remerciements

Merci à tous les contributeurs ! Chaque contribution, petite ou grande, est précieuse. 🙏

Votre nom sera ajouté à la liste des contributeurs dans le README.

---

**Prêt à contribuer ?** Trouvez une [issue](https://github.com/votre-username/extracteur-factures-pdf/issues) qui vous intéresse et lancez-vous ! 🚀
