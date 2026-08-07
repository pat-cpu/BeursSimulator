"""
=====================================================
BeursSimulator

Bestand : types.py

Constanten en enumeraties.
=====================================================
"""

from enum import Enum


class ProductType(Enum):

    ETF = "ETF"
    AANDEEL = "Aandeel"
    TURBO_LONG = "Turbo Long"
    TURBO_SHORT = "Turbo Short"