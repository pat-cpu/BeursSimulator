"""
BeursSimulator

Bestand : transactie.py

Eén aankoop- of verkooptransactie.
"""

from datetime import datetime


class Transactie:

    def __init__(
        self,
        soort: str,
        ticker: str,
        naam: str,
        aantal: float,
        koers: float,
        datum=None,
        producttype: str = "ETF",
        turbo_soort: str = "",
        stoploss: float = 0.0,
        hefboom: float = 0.0,
        onderliggende_koers: float = 0.0
    ):

        if datum is None:
            self.datum = datetime.now()
        else:
            self.datum = datum

        self.soort = soort.upper()
        self.ticker = ticker.upper()
        self.naam = naam

        self.aantal = aantal
        self.koers = koers

        self.bedrag = aantal * koers

        self.producttype = producttype.upper()
        self.turbo_soort = turbo_soort.upper()
        self.stoploss = stoploss
        self.hefboom = hefboom
        self.onderliggende_koers = onderliggende_koers

        
    def __str__(self) -> str:

        return (
            f"{self.datum:%d/%m/%Y %H:%M:%S} | "
            f"{self.soort:8} | "
            f"{self.ticker:6} | "
            f"{self.aantal:8.2f} | "
            f"€{self.koers:8.2f} | "
            f"€{self.bedrag:10.2f}"
        )