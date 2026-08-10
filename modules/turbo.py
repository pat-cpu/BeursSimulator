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
        hefboom: float,
        onderliggende_koers: float = 0.0
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


        if onderliggende_koers > 0:

            if (
                soort == "LONG"
                and stoploss >= onderliggende_koers
            ):
                raise ValueError(
                    "Bij een Turbo LONG moet de stoploss "
                    "lager zijn dan de onderliggende koers."
                )

            if (
                soort == "SHORT"
                and stoploss <= onderliggende_koers
            ):
                raise ValueError(
                    "Bij een Turbo SHORT moet de stoploss "
                    "hoger zijn dan de onderliggende koers."
                )       
    

        self.soort = soort
        self.stoploss = stoploss
        self.hefboom = hefboom
        self.onderliggende_koers = onderliggende_koers

    def afstand_tot_stoploss(self) -> float:

        if self.onderliggende_koers <= 0:
            return 0.0

        if self.soort == "LONG":

            return (
                (
                    self.onderliggende_koers
                    - self.stoploss
                )
                / self.onderliggende_koers
            ) * 100

        return (
            (
                self.stoploss
                - self.onderliggende_koers
            )
            / self.onderliggende_koers
        ) * 100

    def stoploss_waarschuwing(self) -> bool:

        afstand = self.afstand_tot_stoploss()

        return afstand <= 5

    def risicoklasse(self) -> str:

        afstand = self.afstand_tot_stoploss()

        if afstand < 5:
            return "HOOG RISICO"

        if afstand <= 10:
            return "OPGELET"

        return "VEILIGER"