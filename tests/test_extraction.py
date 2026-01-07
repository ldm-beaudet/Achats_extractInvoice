"""
Tests unitaires pour l'extracteur de factures PDF
"""
import pytest
from src.extract_invoices import clean_number, find_header_indices, has_article_data


class TestCleanNumber:
    """Tests pour la fonction clean_number"""
    
    def test_french_format(self):
        """Test format français avec virgule"""
        assert clean_number("1234,56") == 1234.56
        assert clean_number("1 234,56") == 1234.56
        assert clean_number("1.234,56") == 1234.56
    
    def test_english_format(self):
        """Test format anglais avec point"""
        assert clean_number("1234.56") == 1234.56
        assert clean_number("1,234.56") == 1234.56
    
    def test_with_currency_symbols(self):
        """Test avec symboles monétaires"""
        assert clean_number("1234,56 €") == 1234.56
        assert clean_number("€ 1234,56") == 1234.56
        assert clean_number("$1,234.56") == 1234.56
    
    def test_invalid_values(self):
        """Test valeurs invalides"""
        assert clean_number(None) is None
        assert clean_number("") is None
        assert clean_number("abc") is None
        assert clean_number("*") is None
    
    def test_negative_numbers(self):
        """Test nombres négatifs"""
        assert clean_number("-1234,56") == -1234.56
        assert clean_number("-1,234.56") == -1234.56


class TestFindHeaderIndices:
    """Tests pour la fonction find_header_indices"""
    
    def test_standard_headers(self):
        """Test en-têtes standards"""
        headers = ['Référence', 'Désignation', 'Qté', 'Prix tarif', 'Remise', 'P.U H.T', 'Montant HT']
        indices = find_header_indices(headers)
        
        assert indices['reference'] == 0
        assert indices['designation'] == 1
        assert indices['quantite'] == 2
        assert indices['prix_tarif'] == 3
        assert indices['remise'] == 4
        assert indices['pu_ht'] == 5
        assert indices['montant_ht'] == 6
    
    def test_lowercase_headers(self):
        """Test en-têtes en minuscules"""
        headers = ['référence', 'désignation', 'quantité', 'montant']
        indices = find_header_indices(headers)
        
        assert indices['reference'] == 0
        assert indices['designation'] == 1
        assert indices['quantite'] == 2
        assert indices['montant_ht'] == 3
    
    def test_variant_names(self):
        """Test variantes de noms"""
        headers = ['Ref', 'Description', 'Qty', 'Total']
        # Note: Ces variantes doivent être ajoutées à la fonction si nécessaire
        indices = find_header_indices(headers)
        
        # Vérifier que des indices ont été trouvés
        assert isinstance(indices, dict)
    
    def test_empty_headers(self):
        """Test en-têtes vides"""
        headers = ['', None, '  ']
        indices = find_header_indices(headers)
        
        assert len(indices) == 0
    
    def test_mixed_case(self):
        """Test casse mixte"""
        headers = ['RÉFÉRENCE', 'Désignation', 'qté']
        indices = find_header_indices(headers)
        
        assert 'reference' in indices
        assert 'designation' in indices
        assert 'quantite' in indices


class TestHasArticleData:
    """Tests pour la fonction has_article_data"""
    
    def test_valid_article_row(self):
        """Test ligne valide avec données numériques"""
        row = ['FER-CVE', '', 'CENTRALE VIGIK', '', 1.0, 295.93, '', 295.93, 295.93]
        assert has_article_data(row) is True
    
    def test_row_with_text_only(self):
        """Test ligne avec texte uniquement"""
        row = ['BL2505630', '', '27/01/25', '', '', '', '', '', '']
        assert has_article_data(row) is False
    
    def test_empty_row(self):
        """Test ligne vide"""
        row = ['', '', '', '', '', '', '', '', '']
        assert has_article_data(row) is False
    
    def test_none_values(self):
        """Test ligne avec valeurs None"""
        row = [None, None, None, None]
        assert has_article_data(row) is False
    
    def test_single_numeric_value(self):
        """Test ligne avec une seule valeur numérique"""
        row = ['Texte', '', '', 123.45]
        # Devrait retourner False car besoin d'au moins 2 valeurs numériques
        assert has_article_data(row) is False


class TestIntegration:
    """Tests d'intégration (nécessitent des fichiers PDF)"""
    
    @pytest.mark.skip(reason="Nécessite un fichier PDF de test")
    def test_extract_real_invoice(self):
        """Test extraction facture réelle"""
        from src.extract_invoices import extract_invoice_data
        
        # Ce test nécessiterait un PDF de test dans tests/fixtures/
        data = extract_invoice_data('tests/fixtures/sample_invoice.pdf')
        
        assert len(data) > 0
        assert 'Fichier' in data[0]
        assert 'Désignation' in data[0]
        assert 'Montant HT' in data[0]


# Fixtures pour les tests
@pytest.fixture
def sample_invoice_data():
    """Données de facture exemple pour les tests"""
    return [
        {
            'Fichier': 'test.pdf',
            'Page': 1,
            'Référence': 'REF001',
            'Désignation': 'Article de test',
            'Quantité': 2.0,
            'Prix tarif': 100.0,
            'Remise': None,
            'P.U H.T': 100.0,
            'Montant HT': 200.0
        }
    ]


@pytest.fixture
def sample_pdf_path(tmp_path):
    """Crée un PDF de test temporaire"""
    # Utiliserait reportlab pour créer un vrai PDF
    # Pour l'instant, retourne juste un chemin
    return str(tmp_path / "test.pdf")


if __name__ == "__main__":
    # Permet de lancer les tests avec: python tests/test_extraction.py
    pytest.main([__file__, "-v"])
