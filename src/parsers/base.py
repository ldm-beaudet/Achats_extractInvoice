"""
Classe de base pour tous les parsers de factures
"""
from abc import ABC, abstractmethod
from pathlib import Path


class BaseInvoiceParser(ABC):
    """Classe abstraite pour les parsers de factures"""
    
    def __init__(self):
        self.supplier_name = "Unknown"
    
    @abstractmethod
    def can_parse(self, text_content):
        """
        Détermine si ce parser peut traiter ce PDF
        
        Args:
            text_content: Contenu textuel de la première page du PDF
            
        Returns:
            bool: True si ce parser peut traiter ce PDF
        """
        pass
    
    @abstractmethod
    def extract(self, pdf_path):
        """
        Extrait les données de la facture
        
        Args:
            pdf_path: Chemin vers le PDF
            
        Returns:
            list: Liste de dictionnaires avec les données extraites
                  Format: [{
                      'Fournisseur': str,
                      'Fichier': str,
                      'Page': int,
                      'Référence': str,
                      'Désignation': str,
                      'Quantité': float,
                      'Montant HT': float,
                      ... (autres colonnes spécifiques au fournisseur)
                  }]
        """
        pass
    
    def get_supplier_name(self):
        """Retourne le nom du fournisseur"""
        return self.supplier_name
