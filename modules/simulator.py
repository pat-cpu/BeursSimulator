"""
=====================================================
BeursSimulator

Bestand : simulator.py

Centrale klasse van de BeursSimulator.
=====================================================
"""

from config.instellingen import (
    VERSIE,
    STARTKAPITAAL
)

from modules.logger import logger
from modules.portefeuille import Portefeuille
from modules.transactieregister import TransactieRegister


class BeursSimulator:

    def __init__(self):

        logger.info(
            "BeursSimulator initialiseren..."
        )

        self.versie = VERSIE
        self.startkapitaal = STARTKAPITAAL

        # Eén centraal transactieregister
        self.transactieregister = (
            TransactieRegister()
        )

        # Portefeuille gebruikt hetzelfde register
        self.portefeuille = Portefeuille(
            startkapitaal=self.startkapitaal,
            transactieregister=self.transactieregister
        )

        logger.info(
            "Startkapitaal : €%.2f",
            self.portefeuille.cash
        )

    def info(self):

        logger.info("")
        logger.info(
            "========== STATUS =========="
        )

        logger.info(
            "Versie          : %s",
            self.versie
        )

        logger.info(
            "Cash            : €%.2f",
            self.portefeuille.cash
        )

        logger.info(
            "Aantal posities : %d",
            self.portefeuille.aantal_posities()
        )

        logger.info(
            "Transacties     : %d",
            self.transactieregister.aantal()
        )

        logger.info(
            "============================"
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

        self.portefeuille.koop(
            positie=positie,
            aantal=aantal,
            koers=koers
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

        self.portefeuille.verkoop(
            ticker=ticker,
            aantal=aantal,
            koers=koers
        )

    # ==================================================
    # OVERZICHTEN
    # ==================================================

    def toon_portefeuille(self):

        logger.info("")
        logger.info(
            "========== PORTEFEUILLE =========="
        )

        logger.info(
            "Cash : €%.2f",
            self.portefeuille.cash
        )

        for positie in self.portefeuille.posities.values():

            logger.info(
                "%-6s %8.2f stuks @ €%.2f",
                positie.ticker,
                positie.aantal,
                positie.gemiddelde_koers
            )

    def toon_transacties(self):

        self.transactieregister.print_overzicht()

     # ==================================================
    # BEWAREN
    # ==================================================

    def bewaar_transacties(
        self,
        bestandsnaam: str = "transacties.csv"
    ) -> None:

        self.transactieregister.export_csv(
            bestandsnaam
        )       