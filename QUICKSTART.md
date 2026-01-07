# 🚀 DÉMARRAGE RAPIDE - 5 MINUTES

Guide ultra-rapide pour commencer à utiliser l'extracteur de factures PDF.

## ⚡ Installation express

```bash
# 1. Extraire l'archive
tar -xzf extracteur-factures-pdf.tar.gz
cd extracteur-factures-pdf

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Tester avec une facture de démo
python examples/create_demo_invoice.py
python src/extract_invoices.py facture_demo.pdf

# 4. Vérifier le résultat
ls -l factures_extraites.xlsx
```

## 💡 Premier test avec vos factures

```bash
# Copier vos factures dans le dossier
cp /chemin/vers/vos/factures/*.pdf .

# Extraire
python src/extract_invoices.py *.pdf

# Ouvrir le résultat dans Excel
open factures_extraites.xlsx  # macOS
# ou
start factures_extraites.xlsx  # Windows
# ou
xdg-open factures_extraites.xlsx  # Linux
```

## 📋 Ce que vous obtenez

Un fichier Excel avec ces colonnes :
- **Fichier** : Nom du PDF
- **Page** : Numéro de page
- **Référence** : Code article
- **Désignation** : Description
- **Quantité** : Qté commandée
- **Prix tarif** : Prix catalogue
- **P.U H.T** : Prix unitaire HT
- **Montant HT** : Total HT

## 🎯 Commandes essentielles

```bash
# Une facture
python src/extract_invoices.py ma_facture.pdf

# Plusieurs factures
python src/extract_invoices.py facture1.pdf facture2.pdf facture3.pdf

# Toutes les factures d'un dossier
python src/extract_invoices.py /chemin/*.pdf

# Avec exemple avancé (statistiques + rapports)
python examples/advanced_usage.py
```

## 🔧 Si ça ne marche pas

### Erreur : "pip n'est pas reconnu"
```bash
python -m pip install -r requirements.txt
```

### Erreur : "python n'est pas reconnu"
Installez Python depuis [python.org](https://www.python.org/downloads/)

### Aucune donnée extraite
- Vérifiez que votre PDF contient du texte (pas une image scannée)
- Consultez [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

### Le fichier Excel n'ouvre pas
- Fermez Excel si déjà ouvert
- Vérifiez les permissions du dossier

## 📚 Où trouver de l'aide ?

1. **Documentation basique** : [README.md](README.md)
2. **Installation détaillée** : [docs/INSTALLATION.md](docs/INSTALLATION.md)
3. **Guide d'utilisation** : [docs/USAGE.md](docs/USAGE.md)
4. **Problèmes** : [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
5. **Comprendre la structure** : [STRUCTURE_EXPLAINED.md](STRUCTURE_EXPLAINED.md)

## 🎓 Prochaines étapes

### Pour utilisateurs

1. ✅ Tester avec vos factures
2. ✅ Vérifier les résultats dans Excel
3. ✅ Lire [docs/USAGE.md](docs/USAGE.md) pour plus d'options
4. ✅ Créer un script mensuel (voir examples/)

### Pour développeurs

1. ✅ Lire [STRUCTURE_EXPLAINED.md](STRUCTURE_EXPLAINED.md)
2. ✅ Explorer le code dans `src/`
3. ✅ Lancer les tests : `pytest tests/`
4. ✅ Lire [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 🌟 Mettre sur GitHub

```bash
# 1. Créer un repo sur GitHub
# 2. Lier votre projet local
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/votre-username/extracteur-factures-pdf.git
git push -u origin main
```

Guide détaillé : [GITHUB_SETUP.md](GITHUB_SETUP.md)

## ✅ Checklist de vérification

- [ ] Python installé (version 3.6+)
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Facture de démo créée et extraite avec succès
- [ ] Fichier Excel généré et lisible
- [ ] Testé avec une de vos vraies factures

## 🎉 Vous êtes prêt !

Tout fonctionne ? Parfait ! Vous pouvez maintenant :
- Traiter toutes vos factures
- Automatiser le processus mensuel
- Personnaliser le script selon vos besoins
- Contribuer au projet si vous voulez

---

**Besoin d'aide ?** Consultez la documentation complète ou ouvrez une issue sur GitHub !

**Rappel** : Ce projet est testé et validé sur vos factures GDV. Il devrait fonctionner immédiatement ! 🚀
