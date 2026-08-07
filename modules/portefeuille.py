"""
=====================================================
BeursSimulator

Bestand : portefeuille.py

Beheer van alle posities en cash in de portefeuille.
=====================================================
"""

from modules import transactieregister
from modules.logger import logger
from modules.transactie import Transactie
from modules.transactieregister import TransactieRegister


class Portefeuille:

    def __init__(
        self,
        startkapitaal: float,
        transactieregister=None
    ):

        if startkapitaal < 0:
            raise ValueError(
                "Startkapitaal kan niet negatief zijn."
            )

        self.startkapitaal = startkapitaal
        self.cash = startkapitaal
        self.posities = {}

        if transactieregister is None:
            self.transactieregister = TransactieRegister()
        else:
            self.transactieregister = transactieregister

        logger.info(
            "Portefeuille aangemaakt met startkapitaal €%.2f",
            self.startkapitaal
        )

    # ==================================================
    # CASH
    # ==================================================

    def boek_af(self, bedrag: float) -> None:
        """
        Boekt een bedrag af van de beschikbare cash.
        """

        if bedrag <= 0:
            raise ValueError(
                "Af te boeken bedrag moet groter zijn dan nul."
            )

        if bedrag > self.cash:
            raise ValueError(
                "Onvoldoende cash beschikbaar."
            )

        self.cash -= bedrag

        logger.info(
            "Cash afgeboekt: €%.2f | Nieuwe cash: €%.2f",
            bedrag,
            self.cash
        )

    def boek_bij(self, bedrag: float) -> None:
        """
        Boekt een bedrag bij op de beschikbare cash.
        """

        if bedrag <= 0:
            raise ValueError(
                "Bij te boeken bedrag moet groter zijn dan nul."
            )

        self.cash += bedrag

        logger.info(
            "Cash bijgeboekt: €%.2f | Nieuwe cash: €%.2f",
            bedrag,
            self.cash
        )

    # ==================================================
    # POSITIES
    # ==================================================

    def voeg_positie_toe(self, positie) -> None:
        """
        Voegt een nieuwe positie toe.
        """

        ticker = positie.ticker

        if ticker in self.posities:
            raise ValueError(
                f"Positie {ticker} bestaat al."
            )

        self.posities[ticker] = positie

        logger.info(
            "Nieuwe positie toegevoegd: %s",
            ticker
        )

    def zoek_positie(self, ticker: str):
        """
        Zoekt een positie op ticker.
        """

        return self.posities.get(
            ticker.upper()
        )

    # ==================================================
    # KOPEN
    # ==================================================

    def koop(
        self,
        positie,
        aantal: float,
        koers: float
    ) -> None:
        """
        Koopt een positie en boekt de benodigde cash af.
        """

        if aantal <= 0:
            raise ValueError(
                "Aantal moet groter zijn dan nul."
            )

        if koers <= 0:
            raise ValueError(
                "Koers moet groter zijn dan nul."
            )

        bedrag = aantal * koers

        if bedrag > self.cash:
            raise ValueError(
                "Onvoldoende cash voor deze aankoop."
            )

        bestaande = self.zoek_positie(
            positie.ticker
        )

        self.boek_af(
            bedrag
        )

        if bestaande is None:

            positie.koop(
                aantal,
                koers
            )

            self.voeg_positie_toe(
                positie
            )

        else:

            bestaande.koop(
                aantal,
                koers
            )
        transactie = Transactie(
            soort="KOOP",
            ticker=positie.ticker,
            naam=positie.naam,
            aantal=aantal,
            koers=koers
        )

        self.transactieregister.voeg_toe(
            transactie
        )

        logger.info(
            "Aankoop verwerkt: %s %.2f stuks aan €%.2f",
            positie.ticker,
            aantal,
            koers
        )

# ==================================================
# VERKOPEN
# ==================================================

    def verkoop(
        self,
        ticker: str,
        aantal: float,
        koers: float
    ) -> None:
        """
        Verkoopt een aantal stuks van een bestaande positie
        en boekt de verkoopopbrengst bij op de cash.
        """

        if aantal <= 0:
            raise ValueError(
                "Aantal moet groter zijn dan nul."
            )

        if koers <= 0:
            raise ValueError(
                "Koers moet groter zijn dan nul."
            )

        positie = self.zoek_positie(
            ticker
        )

        if positie is None:
            raise ValueError(
                f"Positie {ticker.upper()} bestaat niet."
            )

        if aantal > positie.aantal:
            raise ValueError(
                "Onvoldoende stuks in portefeuille."
            )

        opbrengst = aantal * koers

        positie.verkoop(
            aantal
        )

        self.boek_bij(
            opbrengst
        )

        transactie = Transactie(
            soort="VERKOOP",
            ticker=positie.ticker,
            naam=positie.naam,
            aantal=aantal,
            koers=koers
        )

        self.transactieregister.voeg_toe(
            transactie
        )

        if positie.aantal == 0:
            del self.posities[positie.ticker]

            logger.info(
                "Positie volledig verkocht en verwijderd: %s",
                positie.ticker
            )

        logger.info(
            "Verkoop verwerkt: %s %.2f stuks aan €%.2f",
            ticker.upper(),
            aantal,
            koers
        )



    # ==================================================
    # OPBOUWEN UIT TRANSACTIES
    # ==================================================

    def opbouwen_uit_transacties(
        self,
        transactieregister
    ) -> None:
        """
        Bouwt de portefeuille opnieuw op
        vanuit een transactieregister.
        """

        self.cash = self.startkapitaal
        self.posities = {}

        for transactie in transactieregister.transacties:

            if transactie.soort == "KOOP":

                positie = self.zoek_positie(
                    transactie.ticker
                )

                if positie is None:
                    from modules.etf import ETF

                    positie = ETF(
                        transactie.ticker,
                        transactie.naam
                    )

                self.koop(
                    positie=positie,
                    aantal=transactie.aantal,
                    koers=transactie.koers
                )

            elif transactie.soort == "VERKOOP":

                self.verkoop(
                    ticker=transactie.ticker,
                    aantal=transactie.aantal,
                    koers=transactie.koers
                )




    # ==================================================
    # BEREKENINGEN
    # ==================================================

    def totaal_aankoopwaarde(self) -> float:

        return sum(
            positie.aankoopwaarde
            for positie in self.posities.values()
        )

    def totale_actuele_waarde(self) -> float:

        return sum(
            positie.actuele_waarde
            for positie in self.posities.values()
        )

    def totale_winst(self) -> float:

        return (
            self.totale_actuele_waarde()
            - self.totaal_aankoopwaarde()
        )

    def totale_portefeuillewaarde(self) -> float:

        return (
            self.cash
            + self.totale_actuele_waarde()
        )

    def aantal_posities(self) -> int:

        return len(self.posities)