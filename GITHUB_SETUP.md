# 🚀 Guide d'initialisation Git et GitHub

Ce fichier vous guide pour publier votre projet sur GitHub.

## Étape 1 : Initialiser Git localement

```bash
# Se placer dans le dossier du projet
cd Achats_extractInvoice

# Initialiser Git
git init

# Configurer votre identité (si première fois)
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit: Achats_extractInvoice PDF v2.0"
```

## Étape 2 : Créer un repository sur GitHub

1. **Allez sur GitHub** : https://github.com
2. **Cliquez sur "New repository"** (bouton vert en haut à droite)
3. **Remplissez** :
   - **Repository name** : `Achats_extractInvoice`
   - **Description** : "Outil Python pour extraire automatiquement les données des factures PDF vers Excel"
   - **Public** ou **Private** : À votre choix
   - **NE PAS** cocher "Initialize with README" (on en a déjà un)
4. **Cliquez sur "Create repository"**

## Étape 3 : Lier votre projet local à GitHub

```bash
# Remplacer 'votre-username' par votre nom d'utilisateur GitHub
git remote add origin https://github.com/votre-username/Achats_extractInvoice.git

# Vérifier la connexion
git remote -v

# Pousser votre code sur GitHub
git branch -M main
git push -u origin main
```

**Si vous utilisez SSH** (recommandé) :
```bash
git remote add origin git@github.com:votre-username/Achats_extractInvoice.git
git push -u origin main
```

## Étape 4 : Vérifier sur GitHub

Retournez sur GitHub et actualisez la page. Vous devriez voir tous vos fichiers !

## Étapes suivantes (optionnel)

### Ajouter des badges au README

Les badges donnent des infos visuelles sur votre projet.

```markdown
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

### Activer GitHub Actions (CI/CD)

Créez `.github/workflows/tests.yml` :

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.6, 3.7, 3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=src
```

### Protéger la branche main

1. **Settings** → **Branches**
2. **Add rule** pour `main`
3. Cocher "Require pull request reviews before merging"

### Créer des templates d'issues

GitHub peut avoir des templates pour :
- Bug reports
- Feature requests

Créez `.github/ISSUE_TEMPLATE/bug_report.md` et `feature_request.md`

### Ajouter un CHANGELOG

Créez `CHANGELOG.md` pour documenter les changements :

```markdown
# Changelog

## [2.0.0] - 2026-01-07
### Added
- Détection intelligente des tableaux complexes
- Support des factures GDV
- Export Excel avec toutes les colonnes
- Documentation complète

### Changed
- Amélioration de l'algorithme d'extraction
- Filtrage automatique des lignes parasites

## [1.0.0] - 2025-12-XX
### Added
- Version initiale basique
```

## Workflow Git quotidien

### Avant de commencer à travailler

```bash
# Récupérer les dernières modifications
git pull origin main
```

### Pendant le travail

```bash
# Voir les modifications
git status

# Ajouter des fichiers
git add fichier.py
# ou tout ajouter
git add .

# Commiter
git commit -m "Description de vos changements"
```

### Partager votre travail

```bash
# Pousser vers GitHub
git push origin main
```

### Créer une nouvelle fonctionnalité

```bash
# Créer une branche
git checkout -b feature/ma-fonctionnalite

# Travailler sur la branche
# ... modifications ...
git add .
git commit -m "Ajout de ma fonctionnalité"

# Pousser la branche
git push origin feature/ma-fonctionnalite

# Sur GitHub, créer une Pull Request
```

## Commandes Git utiles

```bash
# Voir l'historique
git log --oneline

# Annuler le dernier commit (mais garder les changements)
git reset --soft HEAD~1

# Voir les différences
git diff

# Changer de branche
git checkout nom-branche

# Supprimer une branche locale
git branch -d nom-branche

# Synchroniser avec GitHub
git fetch origin
git pull origin main
```

## Problèmes courants

### Erreur : "fatal: remote origin already exists"

**Solution** :
```bash
git remote remove origin
git remote add origin https://github.com/votre-username/Achats_extractInvoice.git
```

### Erreur d'authentification GitHub

**Solution** : Utilisez un Personal Access Token au lieu du mot de passe
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token
3. Utilisez ce token comme mot de passe

### Conflits lors du pull

**Solution** :
```bash
# Voir les fichiers en conflit
git status

# Éditer les fichiers pour résoudre les conflits
# Puis
git add fichier-resolu.py
git commit -m "Résolution des conflits"
```

## Ressources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials)

## Aide

Si vous êtes bloqué :
1. `git status` vous dit toujours où vous en êtes
2. `git help <commande>` affiche l'aide
3. Google votre message d'erreur
4. Demandez de l'aide dans les issues

---

**Félicitations !** Votre projet est maintenant sur GitHub ! 🎉
