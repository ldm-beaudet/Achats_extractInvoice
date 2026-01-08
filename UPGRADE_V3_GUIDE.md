# 🚀 MISE À JOUR MULTI-FOURNISSEURS

## ✨ Nouveau dans la v3.0

Votre extracteur supporte maintenant **PLUSIEURS FOURNISSEURS** automatiquement !

### 📊 Fournisseurs supportés

1. ✅ **GDV** (Le Distributeur Courants Faibles)
2. ✅ **RICHARDSON** (Nouveau!)
3. 🔧 **Facilement extensible** pour d'autres fournisseurs

## 🎯 Ce qui change

### Avant (v2)
```bash
python src/extract_invoices.py factures/*.pdf
# → Ne marchait qu'avec GDV
```

### Maintenant (v3)
```bash
python extract_invoices_v3.py factures/*.pdf
# → Détecte automatiquement GDV, RICHARDSON, etc.
# → Un seul fichier Excel avec TOUS les fournisseurs
```

## 📈 Résultat

Le fichier Excel contient maintenant une colonne **"Fournisseur"** :

| Fournisseur | Fichier | Référence | Désignation | Quantité | Montant HT |
|-------------|---------|-----------|-------------|----------|------------|
| GDV | F250486.pdf | JGI-BCL9300 | CENTRALE VIGIK | 1 | 647,00 |
| RICHARDSON | Richardson_132659.pdf | 9421J2 | LAVE-MAINS ODEON | 2 | 144,34 |

## 🔧 Installation dans votre projet

### Option 1 : Remplacer l'ancien script

```bash
cd Achats_extractInvoice

# Sauvegarder l'ancien
cp src/extract_invoices.py src/extract_invoices_v2_backup.py

# Copier le nouveau
cp extract_invoices_v3.py src/extract_invoices.py
```

### Option 2 : Garder les deux versions

```bash
cd Achats_extractInvoice

# Ajouter v3 à côté de v2
cp extract_invoices_v3.py src/extract_invoices_multi.py

# Utiliser selon besoin
python src/extract_invoices.py        # v2 (GDV seulement)
python src/extract_invoices_multi.py  # v3 (tous fournisseurs)
```

## 🎯 Utilisation

### Extraire toutes vos factures (mix de fournisseurs)

```bash
python extract_invoices_v3.py Factures/*.pdf
```

Le script :
1. ✅ Détecte automatiquement chaque fournisseur
2. ✅ Utilise le bon parser pour chaque facture
3. ✅ Consolide tout dans un seul Excel
4. ✅ Affiche un résumé par fournisseur

### Exemple de sortie

```
Traitement de 10 fichier(s)...

Traitement de: F2504861.pdf
  Type détecté: GDV
  → 1 ligne(s) extraite(s)

Traitement de: Richardson_132659.pdf
  Type détecté: RICHARDSON
  → 4 ligne(s) extraite(s)

✓ Données exportées vers: factures_extraites.xlsx
  Total: 15 ligne(s) extraite(s)

Résumé par fournisseur:
  - GDV: 8 ligne(s)
  - RICHARDSON: 7 ligne(s)
```

## 🆕 Ajouter un nouveau fournisseur

C'est **facile** ! Suivez ce template :

### 1. Ajouter la détection

Dans la fonction `detect_supplier()` :

```python
# Détection Fournisseur X
if 'MOT_CLÉ_UNIQUE' in text_upper:
    return 'FOURNISSEUR_X'
```

### 2. Créer le parser

```python
def extract_fournisseur_x(pdf_path):
    """Extrait les données d'une facture FOURNISSEUR_X"""
    invoice_data = []
    
    # Votre logique d'extraction ici
    # ...
    
    return invoice_data
```

### 3. L'ajouter au switch

Dans `extract_invoice_data()` :

```python
elif supplier == 'FOURNISSEUR_X':
    return extract_fournisseur_x(pdf_path)
```

**C'est tout !** 🎉

## 📚 Architecture du code

```python
# 1. Détection automatique
supplier = detect_supplier(pdf)  # → 'GDV', 'RICHARDSON', etc.

# 2. Utilise le bon parser
if supplier == 'GDV':
    data = extract_gdv(pdf)
elif supplier == 'RICHARDSON':
    data = extract_richardson(pdf)

# 3. Format unifié
# Tous les parsers retournent le même format :
{
    'Fournisseur': 'GDV',
    'Fichier': 'facture.pdf',
    'Référence': 'REF123',
    'Désignation': 'Article',
    'Quantité': 2,
    'Montant HT': 100.00
}
```

## 🔍 Comment ça marche ?

### Parser GDV (existant)
- Cherche des tableaux structurés
- Détecte les en-têtes
- Extrait ligne par ligne

### Parser Richardson (nouveau)
- Analyse le texte brut
- Utilise des regex pour trouver les articles
- Format : `DÉSIGNATION U ... ...72,17 2 ...144,34 CODE`

### Détection automatique
1. Lit la première page
2. Cherche des mots-clés :
   - "LE DISTRIBUTEUR COURANTS FAIBLES" → GDV
   - "RICHARDSON" → Richardson
3. Applique le bon parser

## 💡 Avantages

✅ **Un seul script** pour tous vos fournisseurs
✅ **Détection automatique** - pas besoin de trier
✅ **Consolidation** - un seul fichier Excel
✅ **Évolutif** - ajoutez des fournisseurs facilement
✅ **Rétrocompatible** - fonctionne toujours avec GDV

## 🎓 Pour aller plus loin

### Améliorer la détection Richardson

Le parser Richardson actuel utilise du regex. Pour des structures plus complexes :

```python
# Utiliser pdfplumber pour extraire les tableaux
tables = page.extract_tables()

# Puis parser les cellules
for table in tables:
    for row in table:
        # Logique d'extraction
```

### Ajouter des colonnes spécifiques

Certains fournisseurs ont des infos uniques :

```python
invoice_data.append({
    'Fournisseur': 'RICHARDSON',
    'Numéro_facture': extract_invoice_number(text),  # Nouveau
    'Date_facture': extract_invoice_date(text),      # Nouveau
    'Référence': code,
    # ... autres colonnes
})
```

### Logger les échecs

```python
if not data:
    with open('extraction_errors.log', 'a') as f:
        f.write(f"{pdf_path}: Échec extraction\n")
```

## 📊 Statistiques avancées

Une fois consolidé, analysez facilement :

```python
import pandas as pd

df = pd.read_excel('factures_extraites.xlsx')

# Par fournisseur
print(df.groupby('Fournisseur')['Montant HT'].sum())

# GDV:        1044,28 €
# RICHARDSON:  850,52 €
```

## ✅ Checklist migration

- [ ] Tester v3 avec vos factures actuelles
- [ ] Vérifier que GDV fonctionne toujours
- [ ] Vérifier que Richardson est bien extrait
- [ ] Comparer les résultats v2 vs v3
- [ ] Remplacer dans votre workflow
- [ ] Mettre à jour `extract_all.py` si vous l'utilisez
- [ ] Commit sur GitHub

## 🆘 Problèmes connus

### "Type détecté: UNKNOWN"

Le script n'a pas reconnu le fournisseur. Solutions :
1. Vérifiez le mot-clé dans `detect_supplier()`
2. Ajoutez le fournisseur manuellement
3. Envoyez-moi un exemple pour que je l'ajoute

### Richardson : Articles manquants

Le regex est strict. Si des articles manquent :
- Vérifiez le format dans le PDF
- Ajustez le pattern regex
- Utilisez le mode debug pour voir la structure

### Mix GDV/Richardson : Colonnes vides

Normal ! Certaines colonnes n'existent que pour certains fournisseurs.
Excel affiche `NaN` (Not a Number) pour les valeurs manquantes.

## 🎉 Résumé

**Avant** : Un script par fournisseur
**Maintenant** : Un script universel

**Avant** : Trier les factures manuellement
**Maintenant** : Détection automatique

**Avant** : Fusionner les Excel
**Maintenant** : Tout dans un fichier

**C'est ça, un vrai gain de productivité !** 🚀

---

**Questions ?** Testez d'abord avec vos factures, puis on ajuste si besoin !
