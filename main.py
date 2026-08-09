from modules.logger import logger
from modules.simulator import BeursSimulator
from modules.etf import ETF

def toon_menu() -> None:

    print("")
    print("=" * 40)
    print("        BEURSSIMULATOR")
    print("=" * 40)

    print("1 - Status")
    print("2 - Portefeuille")
    print("3 - Transacties")
    print("4 - ETF kopen")
    print("5 - ETF verkopen")
    print("6 - Transacties bewaren")
    print("0 - Stoppen")


def main() -> None:

    logger.info("=" * 50)
    logger.info("Programma gestart")

    simulator = BeursSimulator()

    while True:

        toon_menu()

        keuze = input(
            "\nKeuze : "
        ).strip()

        if keuze == "1":

            simulator.info()

        elif keuze == "2":

            simulator.toon_portefeuille()

        elif keuze == "3":

            simulator.toon_transacties()
        
        elif keuze == "4":

            print("")
            print("=== ETF KOPEN ===")

            ticker = input(
                "Ticker : "
            ).strip().upper()

            naam = input(
                "Naam   : "
            ).strip()
       
            try:
                aantal = float(
                    input("Aantal : ").replace(",", ".")
                )
            except ValueError:
                print("")
                print(
                    "Fout: Aantal moet een getal zijn."
                )
                continue

            try:
                koers = float(
                    input("Koers  : ").replace(",", ".")
                )
            except ValueError:
                print("")
                print(
                    "Fout: Koers moet een getal zijn."
                )
                continue

            try:
                etf = ETF(
                    ticker,
                    naam
                )

                simulator.koop(
                    positie=etf,
                    aantal=aantal,
                    koers=koers
                )

                print("")
                print(
                    f"Aankoop uitgevoerd: "
                    f"{aantal:.2f} {ticker} aan €{koers:.2f}"
                )

            except ValueError as fout:
                print("")
                print(
                    f"Fout: {fout}"
                )

        elif keuze == "5":

            print("")
            print("=== ETF VERKOPEN ===")

            ticker = input(
                "Ticker : "
            ).strip().upper()

            try:
                aantal = float(
                    input("Aantal : ").replace(",", ".")
                )

            except ValueError:
                print("")
                print(
                    "Fout: Aantal moet een getal zijn."
                )
                continue

            try:
                koers = float(
                    input("Koers  : ").replace(",", ".")
                )

            except ValueError:
                print("")
                print(
                    "Fout: Koers moet een getal zijn."
                )
                continue

            try:
                simulator.verkoop(
                    ticker=ticker,
                    aantal=aantal,
                    koers=koers
                )

                print("")
                print(
                    f"Verkoop uitgevoerd: "
                    f"{aantal:.2f} {ticker} aan €{koers:.2f}"
                )

            except ValueError as fout:
                print("")
                print(
                    f"Fout: {fout}"
                )    

        elif keuze == "6":

            try:
                simulator.bewaar_transacties()

                print("")
                print(
                    "Transacties opgeslagen in transacties.csv"
                )

            except OSError as fout:

                print("")
                print(
                    f"Fout bij bewaren: {fout}"
                )


              

        elif keuze == "0":

            break

        else:

            print("")
            print("Ongeldige keuze.")

    logger.info(
        "Programma beëindigd"
    )


if __name__ == "__main__":
    main()