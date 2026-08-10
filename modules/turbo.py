"""
=====================================================
BeursSimulator

Bestand : turbo.py

Turbo positie voor de BeursSimulator.
=====================================================
"""

from modules.positie import Positie


class Turbo(Positie):

    def __init__(
        self,
        ticker: str,
        naam: str,
        soort: str,
        stoploss: float,
        hefboom: float
    ):

        super().__init__(
            ticker=ticker,
            naam=naam
        )

        soort = soort.upper()

        if soort not in ("LONG", "SHORT"):
            raise ValueError(
                "Turbo soort moet LONG of SHORT zijn."
            )

        if stoploss <= 0:
            raise ValueError(
                "Stoploss moet groter zijn dan nul."
            )

        if hefboom <= 0:
            raise ValueError(
                "Hefboom moet groter zijn dan nul."
            )

        self.soort = soort
        self.stoploss = stoploss
        self.hefboom = hefboom

    def afstand_tot_stoploss(self) -> float:

        if self.huidige_koers <= 0:
            return 0.0

        if self.soort == "LONG":
            return (
                (
                    self.huidige_koers
                    - self.stoploss
                )
                / self.huidige_koers
            ) * 100

        return (
            (
                self.stoploss
                - self.huidige_koers
            )
            / self.huidige_koers
        ) * 100       

    def stoploss_waarschuwing(self) -> bool:

        afstand = self.afstand_tot_stoploss()

        return afstand <= 5  