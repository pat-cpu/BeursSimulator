"""
BeursSimulator

Bestand : transactieregister.py

Beheert alle transacties.
"""
import csv

from datetime import datetime

from modules.logger import logger
from modules.transactie import Transactie



class TransactieRegister:

    def __init__(self):

        self.transacties = []


    # ==================================================
    # CSV EXPORT
    # ==================================================

    def export_csv(
        self,
        bestandsnaam: str
    ) -> None:
        """
        Exporteert alle transacties naar een CSV-bestand.
        """

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
                "Datum",
                "Soort",
                "Ticker",
                "Naam",
                "Aantal",
                "Koers",
                "Bedrag"
            ])

            for transactie in self.transacties:

                writer.writerow([
                    transactie.datum.strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),
                    transactie.soort,
                    transactie.ticker,
                    transactie.naam,
                    transactie.aantal,
                    transactie.koers,
                    transactie.bedrag
                ])

        logger.info(
            "Transacties geëxporteerd naar %s",
            bestandsnaam
        )


    # ==================================================
    # CSV IMPORT
    # ==================================================

    def import_csv(
        self,
        bestandsnaam: str
    ) -> None:
        """
        Leest transacties uit een CSV-bestand.
        """

        self.transacties.clear()

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

                datum = datetime.strptime(
                    rij["Datum"],
                    "%d/%m/%Y %H:%M:%S"
                )

                transactie = Transactie(
                    soort=rij["Soort"],
                    ticker=rij["Ticker"],
                    naam=rij["Naam"],
                    aantal=float(rij["Aantal"]),
                    koers=float(rij["Koers"]),
                    datum=datum
                )

                self.transacties.append(
                    transactie
                )

        logger.info(
            "%d transacties geïmporteerd uit %s",
            self.aantal(),
            bestandsnaam
        )



    # ==================================================
    # TOEVOEGEN
    # ==================================================

    def voeg_toe(
        self,
        transactie
    ) -> None:

        self.transacties.append(
            transactie
        )

        logger.info(
            "Transactie geregistreerd: %s %s %.2f",
            transactie.soort,
            transactie.ticker,
            transactie.aantal
        )

    # ==================================================
    # OPVRAGEN
    # ==================================================

    def aantal(self) -> int:

        return len(
            self.transacties
        )

    # ==================================================
    # OVERZICHT
    # ==================================================

    def print_overzicht(self) -> None:

        print("")
        print("=" * 70)
        print("TRANSACTIEREGISTER")
        print("=" * 70)

        if not self.transacties:

            print("Geen transacties.")

            return

        for transactie in self.transacties:

            print(
                transactie
            )