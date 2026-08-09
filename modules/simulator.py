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

import csv


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
# KOERS BIJWERKEN
# ==================================================

    def update_koers(
        self,
        ticker: str,
        koers: float
    ) -> None:

        self.portefeuille.update_koers(
            ticker=ticker,
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

            logger.info("")

            logger.info(
                "%s",
                positie.ticker
            )

            logger.info(
                "  Aantal             : %.2f",
                positie.aantal
            )

            logger.info(
                "  Gem. aankoopkoers  : €%.2f",
                positie.gemiddelde_koers
            )

            logger.info(
                "  Actuele koers      : €%.2f",
                positie.huidige_koers
            )

            logger.info(
                "  Winst/verlies      : €%.2f",
                positie.winst
            )

            logger.info(
                "  Rendement          : %.2f%%",
                positie.rendement
            )

            logger.info(
                "--------------------------------------"
            )

            logger.info(
                "Totale aankoopwaarde      : €%.2f",
                self.portefeuille.totaal_aankoopwaarde()
            )

            logger.info(
                "Totale actuele waarde     : €%.2f",
                self.portefeuille.totale_actuele_waarde()
            )

            logger.info(
                "Totale winst/verlies      : €%.2f",
                self.portefeuille.totale_winst()
            )

            logger.info(
                "Totale waarde incl. cash  : €%.2f",
                self.portefeuille.totale_portefeuillewaarde()
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

    # ==================================================
    # LADEN
    # ==================================================

    def laad_transacties(
        self,
        bestandsnaam: str = "transacties.csv"
    ) -> None:

        self.transactieregister.import_csv(
            bestandsnaam
        )

        self.portefeuille.opbouwen_uit_transacties(
            self.transactieregister
        )

        logger.info(
            "Portefeuille opnieuw opgebouwd uit %s",
            bestandsnaam
        )

        # ==================================================
        # KOERSEN BEWAREN
        # ==================================================

    def bewaar_koersen(
                self,
                bestandsnaam: str = "koersen.csv"
            ) -> None:

                with open(
                    bestandsnaam,
                    "w",
                    newline="",
                    encoding="utf-8-sig"
                ) as csvfile:

                    writer = csv.writer(
                        csvfile,
                        delimiter=";"
                    )

                    writer.writerow([
                        "Ticker",
                        "Koers"
                    ])

                    for positie in self.portefeuille.posities.values():

                        writer.writerow([
                            positie.ticker,
                            positie.huidige_koers
                        ])

                logger.info(
                    "Actuele koersen opgeslagen in %s",
                    bestandsnaam
                )  

    # ==================================================
    # KOERSEN LADEN
    # ==================================================

    def laad_koersen(
        self,
        bestandsnaam: str = "koersen.csv"
    ) -> None:

        with open(
            bestandsnaam,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as csvfile:

            reader = csv.DictReader(
                csvfile,
                delimiter=";"
            )

            for rij in reader:

                ticker = rij["Ticker"]
                koers = float(
                    rij["Koers"]
                )

                self.portefeuille.update_koers(
                    ticker=ticker,
                    koers=koers
                )

        logger.info(
            "Actuele koersen geladen uit %s",
            bestandsnaam
        )                  