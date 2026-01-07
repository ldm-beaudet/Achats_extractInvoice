"""
Extracteur de Factures PDF
Un outil pour extraire automatiquement les données des factures PDF vers Excel
"""

__version__ = "2.0.0"
__author__ = "Votre Nom"
__email__ = "votre.email@example.com"

from .extract_invoices import process_invoices, extract_invoice_data

__all__ = ['process_invoices', 'extract_invoice_data']
