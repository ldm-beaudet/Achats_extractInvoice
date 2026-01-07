# 📚 COMPRENDRE LA STRUCTURE DU PROJET

Ce document explique **pourquoi** chaque fichier existe et **comment** les utiliser. Parfait pour les débutants !

## 🎯 Vue d'ensemble

```
extracteur-factures-pdf/
│
├── 📄 Fichiers de configuration (racine)
├── 📁 src/           → Le code source
├── 📁 examples/      → Exemples d'utilisation
├── 📁 tests/         → Tests automatiques
├── 📁 docs/          → Documentation détaillée
└── 📁 output/        → Dossier pour les résultats
```

## 📄 Fichiers à la racine (pourquoi ils existent)

### README.md
**C'est quoi ?** La page d'accueil de votre projet sur GitHub.

**Pourquoi ?** 
- Première chose que les visiteurs voient
- Explique ce que fait le projet
- Montre comment l'installer

**Quand le modifier ?**
- Ajout de fonctionnalités majeures
- Changement de la façon d'utiliser le script
- Mise à jour des badges

### LICENSE
**C'est quoi ?** La licence du code (ici MIT).

**Pourquoi ?**
- Définit comment les autres peuvent utiliser votre code
- MIT = très permissif, tout le monde peut l'utiliser

**Quand le modifier ?**
- Rarement. Choisissez au début et gardez.

### requirements.txt
**C'est quoi ?** Liste des bibliothèques Python nécessaires.

**Pourquoi ?**
- Permet d'installer tout avec une commande : `pip install -r requirements.txt`
- Spécifie les versions minimales

**Quand le modifier ?**
- Ajout d'une nouvelle bibliothèque
- Mise à jour des versions

**Exemple** :
```txt
pdfplumber>=0.10.0    ← "≥" = version 0.10.0 ou supérieure
pandas>=2.0.0
```

### setup.py
**C'est quoi ?** Configuration pour installer le projet comme un package Python.

**Pourquoi ?**
- Permet `pip install -e .`
- Crée une commande `extract-invoices`
- Utile pour distribuer le package

**Quand le modifier ?**
- Changement de version
- Ajout de dépendances
- Changement d'auteur/description

**Pour débutants** : Pas besoin de toucher au début, c'est optionnel.

### .gitignore
**C'est quoi ?** Liste de fichiers que Git doit ignorer.

**Pourquoi ?**
- Les PDFs et Excel ne doivent pas être versionnés (trop gros, données privées)
- Les fichiers Python compilés (.pyc) ne servent à rien dans Git
- Garde le repository propre

**Contenu typique** :
```
*.pdf         ← Ignorer tous les PDFs
*.xlsx        ← Ignorer tous les Excel
__pycache__/  ← Fichiers Python compilés
venv/         ← Environnement virtuel
```

**Quand le modifier ?**
- Ajout de nouveaux types de fichiers à ignorer

### GITHUB_SETUP.md
**C'est quoi ?** Guide pas-à-pas pour mettre le projet sur GitHub.

**Pourquoi ?**
- Vous n'êtes pas développeur
- GitHub peut être intimidant au début
- Un guide clair aide beaucoup

**Quand l'utiliser ?**
- Quand vous êtes prêt à publier sur GitHub

## 📁 src/ - Le code source

### __init__.py
**C'est quoi ?** Fichier qui fait de `src/` un "package" Python.

**Pourquoi ?**
- Permet `from src.extract_invoices import ...`
- Définit ce qui est "public" dans le package

**Contenu** :
```python
__version__ = "2.0.0"  ← Version du projet
from .extract_invoices import process_invoices  ← Fonction principale
```

**Pour débutants** : Pas besoin d'y toucher, sauf pour changer la version.

### extract_invoices.py
**C'est quoi ?** LE SCRIPT PRINCIPAL ! Tout le code d'extraction.

**Pourquoi ici ?**
- Sépare le code de la documentation
- Plus professionnel
- Facilite l'import : `from src import extract_invoices`

**Fonctions principales** :
```python
extract_invoice_data(pdf_path)  ← Extrait une facture
process_invoices(pdf_files)     ← Traite plusieurs factures
clean_number(value)             ← Nettoie les nombres
find_header_indices(row)        ← Trouve les colonnes
```

**Quand le modifier ?**
- Ajout de fonctionnalités
- Adaptation à de nouveaux formats de factures

## 📁 examples/ - Exemples pratiques

### create_demo_invoice.py
**C'est quoi ?** Crée une facture PDF de test.

**Pourquoi ?**
- Tester sans avoir de vraies factures
- Développer de nouvelles fonctionnalités
- Montrer comment créer des PDFs avec Python

**Utilisation** :
```bash
python examples/create_demo_invoice.py
# → Crée facture_demo.pdf
```

### advanced_usage.py
**C'est quoi ?** Exemple complet avec statistiques et exports multiples.

**Pourquoi ?**
- Montre comment faire un rapport complet
- Base pour vos propres scripts
- Démontre l'utilisation en tant que bibliothèque

**Utilisation** :
```bash
python examples/advanced_usage.py
```

### README.md
**C'est quoi ?** Documentation des exemples.

**Pourquoi ?**
- Explique chaque exemple
- Montre d'autres cas d'usage
- Donne des idées de personnalisation

## 📁 tests/ - Tests automatiques

### test_extraction.py
**C'est quoi ?** Tests pour vérifier que le code fonctionne.

**Pourquoi ?**
- Attrape les bugs avant qu'ils arrivent
- Vérifie que les modifications ne cassent rien
- Documente le comportement attendu

**Structure** :
```python
def test_clean_number_french():
    """Test des nombres français"""
    assert clean_number("1 234,56") == 1234.56
    # ↑ Si faux, le test échoue
```

**Exécuter les tests** :
```bash
pytest tests/
```

**Pour débutants** : Les tests sont optionnels au début, mais très utiles quand le projet grandit.

## 📁 docs/ - Documentation détaillée

### INSTALLATION.md
**C'est quoi ?** Guide d'installation pas-à-pas.

**Pourquoi ?**
- Installation différente selon Windows/Mac/Linux
- Problèmes courants et solutions
- Pour les utilisateurs non-techniques

### USAGE.md
**C'est quoi ?** Guide d'utilisation complet.

**Pourquoi ?**
- Toutes les façons d'utiliser le script
- Exemples de code Python
- Cas d'usage avancés

### TROUBLESHOOTING.md
**C'est quoi ?** Guide de résolution de problèmes.

**Pourquoi ?**
- Liste des erreurs communes
- Solutions étape par étape
- FAQ

### CONTRIBUTING.md
**C'est quoi ?** Guide pour les contributeurs.

**Pourquoi ?**
- Explique comment contribuer au projet
- Standards de code
- Processus de pull request

**Utile si** : Vous rendez le projet public et voulez accepter des contributions.

## 📁 output/ - Dossier de sortie

### .gitkeep
**C'est quoi ?** Fichier vide pour que Git garde le dossier.

**Pourquoi ?**
- Git n'enregistre pas les dossiers vides
- Ce fichier "truque" Git pour garder le dossier
- Les fichiers Excel générés vont ici

**Dans .gitignore** :
```
output/*        ← Ignore tout dans output/
!output/.gitkeep ← SAUF le .gitkeep
```

## 🎓 Comprendre le workflow

### 1. Développement local

```
Vous travaillez
    ↓
Modifiez src/extract_invoices.py
    ↓
Testez avec python src/extract_invoices.py facture.pdf
    ↓
Ça marche ? → Continuez
Ça bug ? → Debuggez
```

### 2. Tests

```
Écrivez du code
    ↓
Écrivez un test dans tests/
    ↓
Lancez pytest
    ↓
Tests passent ? → OK !
Tests échouent ? → Corrigez
```

### 3. Documentation

```
Nouvelle fonctionnalité
    ↓
Mettez à jour README.md (vue d'ensemble)
    ↓
Mettez à jour docs/USAGE.md (détails)
    ↓
Ajoutez un exemple dans examples/
```

### 4. Versioning Git

```
Modifications faites
    ↓
git add .
    ↓
git commit -m "Description"
    ↓
git push origin main
    ↓
GitHub est à jour !
```

## 🆕 Ajouter une fonctionnalité - Checklist

- [ ] Coder la fonctionnalité dans `src/`
- [ ] Ajouter des tests dans `tests/`
- [ ] Créer un exemple dans `examples/`
- [ ] Documenter dans `docs/USAGE.md`
- [ ] Mettre à jour le `README.md` si majeur
- [ ] Incrémenter la version dans `setup.py`
- [ ] Commit et push

## 📊 Quelle structure pour quel niveau ?

### Débutant (vous)
**Utilisez** :
- src/extract_invoices.py (le script principal)
- README.md (pour GitHub)
- requirements.txt
- .gitignore

**Ignorez** (pour l'instant) :
- Tests (apprendrez plus tard)
- setup.py (optionnel)

### Intermédiaire
**Ajoutez** :
- Tests basiques
- Documentation détaillée
- Exemples variés

### Avancé
**Ajoutez** :
- CI/CD (GitHub Actions)
- Type hints partout
- Couverture de tests >80%
- Documentation API complète

## 💡 Conseils pour débuter

1. **Commencez simple** : Utilisez juste src/ et README.md
2. **Ajoutez progressivement** : Tests → Documentation → Setup
3. **Copiez des exemples** : Regardez d'autres projets Python sur GitHub
4. **Demandez de l'aide** : La communauté Python est très accueillante

## 📚 Ressources pour apprendre

- **Structure Python** : [Real Python - Project Structure](https://realpython.com/python-application-layouts/)
- **Git/GitHub** : [GitHub Guides](https://guides.github.com/)
- **Tests** : [PyTest Tutorial](https://docs.pytest.org/en/stable/getting-started.html)
- **Documentation** : [Write the Docs](https://www.writethedocs.org/)

## ❓ Questions fréquentes

**Q : Dois-je tout créer d'un coup ?**
R : Non ! Commencez avec src/ et README.md, ajoutez le reste progressivement.

**Q : Les tests sont-ils obligatoires ?**
R : Non, mais très recommandés dès que le projet grandit.

**Q : Puis-je simplifier la structure ?**
R : Oui ! Gardez juste ce dont vous avez besoin.

**Q : Comment savoir quoi mettre où ?**
R : Règle simple :
- Code → src/
- Exemples → examples/
- Tests → tests/
- Documentation → docs/
- Config → racine

---

**Félicitations !** 🎉 Vous comprenez maintenant pourquoi chaque fichier existe. La structure peut sembler complexe au début, mais elle rendra votre projet bien plus professionnel et facile à maintenir !
