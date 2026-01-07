#!/usr/bin/env python3
"""
Script de démonstration - Crée une facture PDF de test
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


def create_demo_invoice():
    """Crée une facture PDF de démonstration"""
    
    filename = "facture_demo.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # En-tête
    title = Paragraph("<b>FACTURE N° 2026-001</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*cm))
    
    # Informations facture
    info_text = """
    <b>Date:</b> 07/01/2026<br/>
    <b>Client:</b> Entreprise ABC<br/>
    <b>Adresse:</b> 123 Rue de la République, 75001 Paris
    """
    info = Paragraph(info_text, styles['Normal'])
    story.append(info)
    story.append(Spacer(1, 1*cm))
    
    # Tableau des articles
    data = [
        ['Libellé', 'Quantité', 'Prix unitaire', 'Montant'],
        ['Ordinateur portable Dell XPS 15', '2', '1299,00 €', '2598,00 €'],
        ['Souris sans fil Logitech MX Master', '5', '89,99 €', '449,95 €'],
        ['Clavier mécanique Corsair K70', '3', '159,90 €', '479,70 €'],
        ['Écran 27" LG UltraFine', '4', '549,00 €', '2196,00 €'],
        ['Casque audio Sony WH-1000XM5', '2', '379,00 €', '758,00 €'],
        ['Hub USB-C Anker 7 ports', '10', '45,50 €', '455,00 €'],
    ]
    
    # Créer le tableau
    table = Table(data, colWidths=[8*cm, 2.5*cm, 3*cm, 3*cm])
    
    # Style du tableau
    table.setStyle(TableStyle([
        # En-tête
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Corps du tableau
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 1*cm))
    
    # Total
    total_text = "<b>TOTAL HT: 6936,65 €</b><br/><b>TVA (20%): 1387,33 €</b><br/><b>TOTAL TTC: 8323,98 €</b>"
    total = Paragraph(total_text, styles['Normal'])
    story.append(total)
    
    # Générer le PDF
    doc.build(story)
    print(f"✓ Facture de démonstration créée: {filename}")
    print(f"  Vous pouvez maintenant tester avec:")
    print(f"  python extract_invoices.py {filename}")


if __name__ == "__main__":
    create_demo_invoice()
