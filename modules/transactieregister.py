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
                "Bedrag",
                "Producttype",
                "TurboSoort",
                "Stoploss",
                "Hefboom",
                "OnderliggendeKoers",
                "Reden",
                "GemiddeldeAankoopkoers",
                "Resultaat",
                "ResultaatProcent"
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
                    transactie.bedrag,
                    transactie.producttype,
                    transactie.turbo_soort,
                    transactie.stoploss,
                    transactie.hefboom,
                    transactie.onderliggende_koers,
                    transactie.reden,
                    transactie.gemiddelde_aankoopkoers,
                    transactie.resultaat,
                    transactie.resultaat_procent
                    
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


                try:
                    datum = datetime.strptime(
                        rij["Datum"],
                        "%d/%m/%Y %H:%M:%S"
                    )

                except ValueError:
                    datum = datetime.strptime(
                        rij["Datum"],
                        "%d/%m/%Y %H:%M"
                    )

              

                transactie = Transactie(
                    soort=rij["Soort"],
                    ticker=rij["Ticker"],
                    naam=rij["Naam"],
                    aantal=float(rij["Aantal"]),
                    koers=float(rij["Koers"]),
                    datum=datum,
                    producttype=rij.get(
                        "Producttype",
                        "ETF"
                    ) or "ETF",
                    turbo_soort=rij.get(
                        "TurboSoort",
                        ""
                    ) or "",
                    stoploss=float(
                        rij.get("Stoploss", 0) or 0
                    ),
                    hefboom=float(
                        rij.get("Hefboom", 0) or 0
                    ),


                     onderliggende_koers=float(
                        rij.get("OnderliggendeKoers", 0) or 0
                    ),
                    reden=rij.get(
                        "Reden",
                        ""
                    ) or "",
                    gemiddelde_aankoopkoers=float(
                        rij.get("GemiddeldeAankoopkoers", 0) or 0
                    ),
                    resultaat=float(
                        rij.get("Resultaat", 0) or 0
                    ),
                    resultaat_procent=float(
                        rij.get("ResultaatProcent", 0) or 0
                    )



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

    # ==================================================
    # HANDELSLOGBOEK TURBO'S
    # ==================================================
      
    def print_turbo_logboek(self) -> None:

        turbo_transacties = [
            transactie
            for transactie in self.transacties
            if transactie.producttype == "TURBO"
        ]

        print("")
        print("=" * 70)
        print("HANDELSLOGBOEK TURBO'S")
        print("=" * 70)

        if not turbo_transacties:

            print("Geen turbo-transacties gevonden.")
            return

        totaal_resultaat = 0.0

        for transactie in turbo_transacties:

            print("")
            print("-" * 70)

            print(
                f"Datum                : "
                f"{transactie.datum:%d/%m/%Y %H:%M:%S}"
            )

            print(
                f"Transactie           : "
                f"{transactie.soort}"
            )

            print(
                f"Turbo                : "
                f"{transactie.ticker} — "
                f"{transactie.turbo_soort}"
            )

            print(
                f"Aantal               : "
                f"{transactie.aantal:.2f}"
            )

            print(
                f"Koers                : "
                f"€{transactie.koers:.2f}"
            )

            print(
                f"Reden                : "
                f"{transactie.reden or '-'}"
            )

            if transactie.soort in (
                "VERKOOP",
                "STOPLOSS"
            ):

                print(
                    f"Gem. aankoopkoers    : "
                    f"€{transactie.gemiddelde_aankoopkoers:.2f}"
                )

                print(
                    f"Resultaat            : "
                    f"€{transactie.resultaat:+.2f}"
                )

                print(
                    f"Resultaat procent    : "
                    f"{transactie.resultaat_procent:+.2f}%"
                )

                totaal_resultaat += (
                    transactie.resultaat
                )

        print("")
        print("=" * 70)

        print(
            f"Totaal gerealiseerd resultaat : "
            f"€{totaal_resultaat:+.2f}"
        )

        print("=" * 70)