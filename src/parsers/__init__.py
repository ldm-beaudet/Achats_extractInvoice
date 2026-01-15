"""
Module de parsers de factures
"""
from .base import BaseInvoiceParser
from .gdv import GDVParser
from .richardson import RichardsonParser
from .rexel import RexelParser
from .lynelec import LynelecParser
from .caparol import CaparolParser
from .clareo import ClareoParser
from .nollet import NolletParser
from .sonepar import SoneparParser
from .bcl_decor import BCLDecorParser
from .pointp import PointPParser

# Liste de tous les parsers disponibles
ALL_PARSERS = [
    GDVParser(),
    RichardsonParser(),
    RexelParser(),
    LynelecParser(),
    CaparolParser(),
    ClareoParser(),
    NolletParser(),
    SoneparParser(),
    BCLDecorParser(),
    PointPParser(),
]

__all__ = [
    'BaseInvoiceParser',
    'GDVParser',
    'RichardsonParser',
    'RexelParser',
    'LynelecParser',
    'CaparolParser',
    'ClareoParser',
    'NolletParser',
    'SoneparParser',
    'BCLDecorParser',
    'PointPParser',
    'ALL_PARSERS',
]
