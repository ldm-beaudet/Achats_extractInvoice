# 📦 Guide d'installation

Ce guide vous accompagne pas à pas pour installer l'extracteur de factures PDF.

## Prérequis

### 1. Python

Vous devez avoir Python 3.6 ou supérieur installé sur votre ordinateur.

**Vérifier si Python est installé :**
```bash
python --version
# ou
python3 --version
```

**Si Python n'est pas installé :**
- **Windows** : Téléchargez depuis [python.org](https://www.python.org/downloads/)
- **macOS** : `brew install python3`
- **Linux** : `sudo apt-get install python3 python3-pip`

### 2. pip

pip est le gestionnaire de paquets Python. Il est normalement installé avec Python.

**Vérifier si pip est installé :**
```bash
pip --version
# ou
pip3 --version
```

## Installation

### Méthode 1 : Installation simple (recommandée pour débuter)

1. **Télécharger le projet**

   ```bash
   # Option A : Avec Git
   git clone https://github.com/votre-username/extracteur-factures-pdf.git
   cd extracteur-factures-pdf
   
   # Option B : Téléchargement manuel
   # Téléchargez le ZIP depuis GitHub et décompressez-le
   ```

2. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

   Si vous rencontrez des problèmes de permissions :
   ```bash
   pip install --user -r requirements.txt
   ```

3. **Tester l'installation**

   ```bash
   python src/extract_invoices.py --help
   ```

   Si tout fonctionne, vous devriez voir le message d'aide !

### Méthode 2 : Installation en tant que package (pour utilisateurs avancés)

Cette méthode permet d'utiliser l'outil depuis n'importe où sur votre système.

1. **Cloner et installer**

   ```bash
   git clone https://github.com/votre-username/extracteur-factures-pdf.git
   cd extracteur-factures-pdf
   pip install -e .
   ```

2. **Utiliser la commande**

   Vous pouvez maintenant utiliser la commande `extract-invoices` depuis n'importe où :
   ```bash
   extract-invoices ma_facture.pdf
   ```

### Méthode 3 : Environnement virtuel (recommandé pour les développeurs)

Un environnement virtuel isole les dépendances du projet.

1. **Créer un environnement virtuel**

   ```bash
   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

3. **Pour sortir de l'environnement virtuel**

   ```bash
   deactivate
   ```

## Dépendances installées

Après l'installation, les packages suivants seront disponibles :

| Package | Version | Utilité |
|---------|---------|---------|
| pdfplumber | ≥0.10.0 | Extraction de données des PDFs |
| pandas | ≥2.0.0 | Manipulation de données |
| openpyxl | ≥3.1.0 | Création de fichiers Excel |
| reportlab | ≥4.0.0 | Génération de PDFs de test |

## Vérification de l'installation

### Test rapide

```bash
# Créer une facture de démonstration
python examples/create_demo_invoice.py

# L'extraire
python src/extract_invoices.py facture_demo.pdf

# Vérifier que le fichier Excel a été créé
ls -l factures_extraites.xlsx
```

Si tout fonctionne, vous devriez avoir un fichier `factures_extraites.xlsx` !

## Problèmes courants

### Erreur : "python n'est pas reconnu"

**Solution** : Python n'est pas dans votre PATH. Réinstallez Python en cochant "Add Python to PATH".

### Erreur : "pip n'est pas reconnu"

**Solution** :
```bash
python -m pip install -r requirements.txt
```

### Erreur : "Permission denied"

**Solution** : Utilisez `--user` pour installer localement :
```bash
pip install --user -r requirements.txt
```

### Erreur lors de l'installation de pdfplumber

**Solution** : Certaines dépendances système peuvent être nécessaires :

**Linux :**
```bash
sudo apt-get install python3-dev
```

**macOS :**
```bash
brew install python3
```

### ImportError après installation

**Solution** : Assurez-vous d'être dans le bon dossier :
```bash
cd extracteur-factures-pdf
python src/extract_invoices.py
```

## Mise à jour

Pour mettre à jour vers la dernière version :

```bash
cd extracteur-factures-pdf
git pull origin main
pip install -r requirements.txt --upgrade
```

## Désinstallation

### Si installé avec -e :
```bash
pip uninstall extracteur-factures-pdf
```

### Si installé normalement :
Supprimez simplement le dossier du projet.

## Support

Si vous rencontrez des problèmes d'installation :
1. Vérifiez que vous utilisez Python 3.6+
2. Consultez les [issues GitHub](https://github.com/votre-username/extracteur-factures-pdf/issues)
3. Ouvrez une nouvelle issue avec les détails de votre erreur

---

**Prochaine étape** : Consultez le [Guide d'utilisation](USAGE.md) pour apprendre à utiliser l'outil !
