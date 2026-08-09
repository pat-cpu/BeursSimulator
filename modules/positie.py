"""
=====================================================
BeursSimulator

Bestand : positie.py

Basisklasse voor alle beleggingen.
=====================================================
"""


class Positie:

    def __init__(self, ticker, naam):

        self.ticker = ticker.upper()
        self.naam = naam

        self.aantal = 0.0
        self.gemiddelde_koers = 0.0
        self.huidige_koers = 0.0

    def koop(self, aantal, koers):
        """
        Voegt een aankoop toe en herberekent
        de gemiddelde aankoopkoers.
        """

        if aantal <= 0:
            raise ValueError(
                "Aantal moet groter zijn dan nul."
            )

        if koers <= 0:
            raise ValueError(
                "Koers moet groter zijn dan nul."
            )

        oude_waarde = (
            self.aantal
            * self.gemiddelde_koers
        )

        nieuwe_waarde = (
            aantal
            * koers
        )

        nieuw_aantal = (
            self.aantal
            + aantal
        )

        self.gemiddelde_koers = (
            oude_waarde + nieuwe_waarde
        ) / nieuw_aantal

        self.aantal = nieuw_aantal

        if self.huidige_koers == 0:
            self.huidige_koers = koers

    def verkoop(self, aantal):
        """
        Verkoopt een aantal stuks.

        De gemiddelde aankoopkoers blijft
        behouden voor de resterende stukken.
        """

        if aantal <= 0:
            raise ValueError(
                "Aantal moet groter zijn dan nul."
            )

        if aantal > self.aantal:
            raise ValueError(
                "Onvoldoende stuks in portefeuille."
            )

        self.aantal -= aantal

        if self.aantal == 0:
            self.gemiddelde_koers = 0.0
            self.huidige_koers = 0.0

    def update_koers(
        self,
        koers: float
    ) -> None:
        """
        Werkt de huidige koers van de positie bij.
        """

        if koers <= 0:
            raise ValueError(
                "Koers moet groter zijn dan nul."
            )

        self.huidige_koers = koers   

    @property
    def aankoopwaarde(self):
        return (
            self.aantal
            * self.gemiddelde_koers
        )

    @property
    def actuele_waarde(self):
        return (
            self.aantal
            * self.huidige_koers
        )

    @property
    def winst(self):
        return (
            self.actuele_waarde
            - self.aankoopwaarde
        )

    @property
    def rendement(self):

        if self.aankoopwaarde == 0:
            return 0.0

        return (
            self.winst
            / self.aankoopwaarde
        ) * 100