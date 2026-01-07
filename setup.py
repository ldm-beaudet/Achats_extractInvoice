"""
Configuration pour l'installation du package
"""
from setuptools import setup, find_packages
from pathlib import Path

# Lire le README pour la description longue
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="Achats_extractInvoice",
    version="2.0.0",
    author="Votre Nom",
    author_email="lionel.beaudet@tbes.fr",
    description="Extracteur automatique de données de factures PDF vers Excel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ldm-beaudet/Achats_extractInvoice",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pdfplumber>=0.10.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "reportlab>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "extract-invoices=src.extract_invoices:main",
        ],
    },
    keywords="pdf invoice facture extraction excel comptabilité",
    project_urls={
        "Bug Reports": "https://github.com/ldm-beaudet/Achats_extractInvoice/issues",
        "Source": "https://github.com/ldm-beaudet/Achats_extractInvoice",
        "Documentation": "https://github.com/ldm-beaudet/Achats_extractInvoice/tree/main/docs",
    },
)
