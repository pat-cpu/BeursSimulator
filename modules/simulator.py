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

import os
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


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

            self.bewaar_historiek()

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
        self.bewaar_historiek()
        
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

        self.bewaar_historiek()

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

            if positie.__class__.__name__ == "Turbo":

                logger.info(
                    "%s — TURBO %s",
                    positie.ticker,
                    positie.soort
                )

            else:

                logger.info(
                    "%s — ETF",
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

            if positie.__class__.__name__ == "Turbo":

                logger.info(
                    "  %-30s: %10s",
                    "Soort",
                    positie.soort
                )

                logger.info(
                    "  Onderliggende koers :           %10.2f",
                    positie.onderliggende_koers
                )
                logger.info(
                    "  %-30s: %10.2f",
                    "Stoploss",
                    positie.stoploss
                )

                logger.info(
                    "  %-30s: %9.2fx",
                    "Hefboom",
                    positie.hefboom
                )

                afstand = positie.afstand_tot_stoploss()

                logger.info(
                    "  %-30s: %9.2f%%",
                    "Afstand tot stoploss",
                    afstand
                )

                risico = positie.risicoklasse()

                logger.info(
                    "  %-30s: %10s",
                    "Risicoklasse",
                    risico
                )

                if positie.stoploss_waarschuwing():

                    logger.warning(
                        "  WAARSCHUWING: STOPLOSS DICHTBIJ!"
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
            # TRANSACTIES TONEN
            # ==================================================
    
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
                "Koers",
                "OnderliggendeKoers"
            ])

            for ticker, positie in self.portefeuille.posities.items():

                onderliggende_koers = getattr(
                    positie,
                    "onderliggende_koers",
                    0.0
                )

                writer.writerow([
                    ticker,
                    positie.huidige_koers,
                    onderliggende_koers
                ])

        logger.info(
            "Koersen opgeslagen in %s",
            bestandsnaam
        )
    
    def bewaar_historiek(
        self,
        bestandsnaam: str = "historiek.csv"
    ) -> None:

        bestand_bestaat = os.path.exists(
            bestandsnaam
        )

        cash = self.portefeuille.cash

        beleggingen = (
            self.portefeuille.totale_actuele_waarde()
        )

        totale_waarde = (
            self.portefeuille.totale_portefeuillewaarde()
        )

        winst_verlies = (
            totale_waarde
            - self.startkapitaal
        )

        rendement = (
            self.portefeuille.totaal_rendement()
        )

        huidige_waarden = [
            f"{cash:.2f}",
            f"{beleggingen:.2f}",
            f"{totale_waarde:.2f}",
            f"{winst_verlies:.2f}",
            f"{rendement:.2f}"
        ]

        # Controleer of de laatste historiekregel
        # dezelfde portefeuillewaarden bevat.
        if bestand_bestaat:

            with open(
                bestandsnaam,
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as csvfile:

                regels = list(
                    csv.reader(
                        csvfile,
                        delimiter=";"
                    )
                )

            if len(regels) > 1:

                laatste_regel = regels[-1]

                if laatste_regel[1:] == huidige_waarden:

                    logger.info(
                        "Historiek ongewijzigd: geen nieuwe regel toegevoegd."
                    )

                    return

        with open(
            bestandsnaam,
            "a",
            newline="",
            encoding="utf-8-sig"
        ) as csvfile:

            writer = csv.writer(
                csvfile,
                delimiter=";"
            )

            if not bestand_bestaat:

                writer.writerow([
                    "Datum",
                    "Cash",
                    "Beleggingen",
                    "Totale waarde",
                    "Winst/verlies",
                    "Rendement"
                ])

            writer.writerow([
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),
                *huidige_waarden
            ])

        logger.info(
            "Historiek bijgewerkt: %s",
            bestandsnaam
        )


    def laad_historiek(
        self,
        bestandsnaam: str = "historiek.csv"
    ) -> list:

        historiek = []

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

                datum_tekst = rij["Datum"]

                try:
                    datum = datetime.strptime(
                        datum_tekst,
                        "%d/%m/%Y %H:%M:%S"
                    )

                except ValueError:
                    datum = datetime.strptime(
                        datum_tekst,
                        "%d/%m/%Y %H:%M"
                    )

                historiek.append({
                    "datum": datum,
                    "cash": float(
                        rij["Cash"]
                    ),
                    "beleggingen": float(
                        rij["Beleggingen"]
                    ),
                    "totale_waarde": float(
                        rij["Totale waarde"]
                    ),
                    "winst_verlies": float(
                        rij["Winst/verlies"]
                    ),
                    "rendement": float(
                        rij["Rendement"]
                    )
                })

        logger.info(
            "%d historiekregels geladen uit %s",
            len(historiek),
            bestandsnaam
        )

        return historiek

    def toon_historiek(self) -> None:

        try:
            historiek = self.laad_historiek()

        except FileNotFoundError as fout:

            print("")
            print(f"Historiekbestand niet gevonden: {fout}")
            return

        if not historiek:

            print("")
            print("Nog geen historiek beschikbaar.")
            return

        print("")
        print("=== PORTEFEUILLEHISTORIEK ===")
        print("")

        for regel in historiek:

            print(
                regel["datum"].strftime("%d/%m/%Y %H:%M"),
                f"| Totaal: €{regel['totale_waarde']:.2f}",
                f"| W/V: €{regel['winst_verlies']:.2f}",
                f"| Rendement: {regel['rendement']:.2f}%"
            )

        return historiek


    # ==================================================
    # GRAFIEK
    # ==================================================

    def toon_historiek_grafiek(self) -> None:

        try:
            historiek = self.laad_historiek()

        except FileNotFoundError:

            print("")
            print("Nog geen historiek beschikbaar.")
            return

        if not historiek:

            print("")
            print("Nog geen historiek beschikbaar.")
            return

        datums = [
            regel["datum"]
            for regel in historiek
        ]

        totale_waarden = [
            regel["totale_waarde"]
            for regel in historiek
        ]

        cash_waarden = [
            regel["cash"]
            for regel in historiek
        ]

        beleggingen_waarden = [
            regel["beleggingen"]
            for regel in historiek
        ]

        plt.figure()

        plt.plot(
            datums,
            totale_waarden,
            marker="o",
            label="Totale waarde"
        )

        plt.plot(
            datums,
            cash_waarden,
            marker="o",
            label="Cash"
        )

        plt.plot(
            datums,
            beleggingen_waarden,
            marker="o",
            label="Beleggingen"
        )

        plt.legend()


        plt.title(
            "Evolutie portefeuille"
        )

        plt.xlabel(
            "Datum"
        )

        plt.ylabel(
            "Totale waarde (€)"
        )

        plt.grid(
            True
        )

        plt.gca().xaxis.set_major_formatter(
            mdates.DateFormatter("%d/%m %H:%M")
        )

        plt.gcf().autofmt_xdate()


        plt.tight_layout()

        plt.show(block=False) 
        plt.pause(0.1)

    def toon_winst_verlies_grafiek(self) -> None:

        try:
            historiek = self.laad_historiek()

        except FileNotFoundError:

            print("")
            print("Nog geen historiek beschikbaar.")
            return

        if not historiek:

            print("")
            print("Nog geen historiek beschikbaar.")
            return

        datums = [
            regel["datum"]
            for regel in historiek
        ]

        winst_verlies = [
            regel["winst_verlies"]
            for regel in historiek
        ]

        plt.figure()

        plt.plot(
            datums,
            winst_verlies,
            marker="o",
            label="Winst/verlies"
        )

        plt.axhline(
            y=0,
            linestyle="--"
        )

        plt.title(
            "Evolutie winst/verlies"
        )

        plt.xlabel(
            "Datum"
        )

        plt.ylabel(
            "Winst/verlies (€)"
        )

        plt.grid(
            True
        )

        plt.legend()

        plt.gca().xaxis.set_major_formatter(
            mdates.DateFormatter("%d/%m %H:%M")
        )

        plt.gcf().autofmt_xdate()

        plt.tight_layout()

        plt.show(block=False)
        plt.pause(0.1)


    def toon_rendement_grafiek(self) -> None:

        try:
            historiek = self.laad_historiek()

        except FileNotFoundError:

            print("")
            print("Nog geen historiek beschikbaar.")
            return

        if not historiek:

            print("")
            print("Nog geen historiek beschikbaar.")
            return

        datums = [
            regel["datum"]
            for regel in historiek
        ]

        rendementen = [
            regel["rendement"]
            for regel in historiek
        ]

        plt.figure()

        plt.plot(
            datums,
            rendementen,
            marker="o",
            label="Rendement"
        )

        plt.axhline(
            y=0,
            linestyle="--"
        )

        plt.title(
            "Evolutie rendement"
        )

        plt.xlabel(
            "Datum"
        )

        plt.ylabel(
            "Rendement (%)"
        )

        plt.grid(
            True
        )

        plt.legend()

        plt.gca().xaxis.set_major_formatter(
            mdates.DateFormatter("%d/%m %H:%M")
        )

        plt.gcf().autofmt_xdate()

        plt.tight_layout()

        plt.show(block=False)
        plt.pause(0.1)

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

                onderliggende_koers = float(
                    rij.get(
                        "OnderliggendeKoers",
                        0
                    ) or 0
                )

                self.portefeuille.update_koers(
                    ticker=ticker,
                    koers=koers
                )

                positie = self.portefeuille.zoek_positie(
                    ticker
                )

                if (
                    positie is not None
                    and positie.__class__.__name__ == "Turbo"
                ):
                    positie.onderliggende_koers = (
                        onderliggende_koers
                    )

        logger.info(
            "Actuele koersen geladen uit %s",
            bestandsnaam
        )                  