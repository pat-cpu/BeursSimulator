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
            "Cash                    : €%10.2f",
            self.portefeuille.cash
        )

        for positie in self.portefeuille.posities.values():

            logger.info("")
            logger.info(
                "%s",
                positie.ticker
            )

            logger.info(
                "  %-30s: %10.2f",
                "Aantal",
                positie.aantal
            )

            logger.info(
                "  %-30s: €%9.2f",
                "Gem. aankoopkoers",
                positie.gemiddelde_koers
            )

            logger.info(
                "  %-30s: €%9.2f",
                "Actuele koers",
                positie.huidige_koers
            )

            logger.info(
                "  %-30s: €%9.2f",
                "Ongerealiseerd winst/verlies",
                positie.winst
            )

            logger.info(
                "  %-30s: %9.2f%%",
                "Rendement",
                positie.rendement
            )

        logger.info(
            "------------------------------------------"
        )

        logger.info(
            "%-30s: €%9.2f",
            "Totale aankoopwaarde",
            self.portefeuille.totaal_aankoopwaarde()
        )

        logger.info(
            "%-30s: €%9.2f",
            "Totale actuele waarde",
            self.portefeuille.totale_actuele_waarde()
        )

        logger.info(
            "%-30s: €%9.2f",
            "Ongerealiseerd winst/verlies",
            self.portefeuille.totale_winst()
        )

        logger.info(
            "%-30s: €%9.2f",
            "Gerealiseerde winst",
            self.portefeuille.gerealiseerde_winst()
        )

        logger.info(
            "%-30s: €%9.2f",
            "Totale winst/verlies",
            self.portefeuille.totale_portefeuillewaarde()
            - self.portefeuille.startkapitaal
        )

        logger.info(
            "%-30s: €%9.2f",
            "Totale waarde incl. cash",
            self.portefeuille.totale_portefeuillewaarde()
        )

        logger.info(
            "%-30s: %9.2f%%",
            "Totaal rendement",
            self.portefeuille.totaal_rendement()
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