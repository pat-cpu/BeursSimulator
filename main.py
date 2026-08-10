from modules.logger import logger
from modules.simulator import BeursSimulator
from modules.etf import ETF

import os
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
    print("7 - Transacties laden")
    print("8 - Actuele koers invoeren")
    print("9 - Historiek")
    print("10 - Grafiek portefeuille")
    print("11 - Grafiek winst/verlies")
    print("12 - Grafiek rendement")
    print("13 - Simulator volledig resetten")
    print("0 - Stoppen")

def main() -> None:

    logger.info("=" * 50)
    logger.info("Programma gestart")


    simulator = BeursSimulator()

    try:
        simulator.laad_transacties()
        simulator.laad_koersen()
        simulator.bewaar_historiek()

        print("")
        print(
            "Bestaande transacties automatisch geladen."
        )

    except FileNotFoundError:

        print("")
        print(
            "Geen bestaand transactiebestand gevonden."
        )

    except (OSError, ValueError) as fout:

        print("")
        print(
            f"Fout bij automatisch laden: {fout}"
        )

    while True:

        toon_menu()

        keuze = input(
            "\nKeuze : "
        ).strip()

        ##################################
        # Keuze 1
        ##################################

        if keuze == "1":

            simulator.info()

        elif keuze == "2":

            simulator.toon_portefeuille()

        elif keuze == "3":

            simulator.toon_transacties()

        ##################################
        # Keuze 4
        ##################################

        elif keuze == "4":

            print("")
            print("=== ETF KOPEN ===")

            ticker = input(
                "Ticker : "
            ).strip().upper()

            if not ticker:

                print("")
                print(
                    "Fout: Ticker mag niet leeg zijn."
                )
                continue

            if not ticker.isalpha():

                print("")
                print(
                    "Fout: Ticker mag alleen letters bevatten."
                )
                continue

            naam = input(
                "Naam   : "
            ).strip()

            if not naam:

                print("")
                print(
                    "Fout: Naam mag niet leeg zijn."
                )
                continue

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

            if aantal <= 0:

                print("")
                print(
                    "Fout: Aantal moet groter zijn dan nul."
                )
                continue

            if koers <= 0:

                print("")
                print(
                    "Fout: Koers moet groter zijn dan nul."
                )
                continue

            bedrag = aantal * koers

            if bedrag > simulator.portefeuille.cash:

                print("")
                print(
                    "Fout: Onvoldoende cash."
                )

                print(
                    f"Beschikbaar : €{simulator.portefeuille.cash:.2f}"
                )

                print(
                    f"Nodig       : €{bedrag:.2f}"
                )

                continue

            print("")
            print("Controle aankoop")

            print("------------------------------")
            print(f"Ticker       : {ticker}")
            print(f"Naam         : {naam}")
            print(f"Aantal       : {aantal:.2f}")
            print(f"Koers        : €{koers:.2f}")
            print(f"Totaalbedrag : €{bedrag:.2f}")
            print("")

            bevestiging = input(
                "Aankoop bevestigen (J/N)? "
            ).strip().upper()

            if bevestiging != "J":

                print("")
                print(
                    "Aankoop geannuleerd."
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
                simulator.bewaar_transacties()
                simulator.bewaar_koersen()
                
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

        ##################################
        # Keuze 5
        ##################################

        elif keuze == "5":

            print("")
            print("=== ETF VERKOPEN ===")

            ticker = input(
                "Ticker : "
            ).strip().upper()

            if not ticker:

                print("")
                print(
                    "Fout: Ticker mag niet leeg zijn."
                )
                continue

            if not ticker.isalpha():

                print("")
                print(
                    "Fout: Ticker mag alleen letters bevatten."
                )
                continue

            positie = simulator.portefeuille.zoek_positie(
                ticker
            )

            if positie is None:

                print("")
                print(
                    f"Fout: Positie {ticker} bestaat niet."
                )
                continue

            print("")
            print(
            f"Beschikbaar: {positie.aantal:.2f} stuks {ticker}"
            )

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

            # Controle aantal te verkopen stuks
            if aantal <= 0:

                print("")
                print(
                    "Fout: Aantal moet groter zijn dan nul."
                )
                continue

            if aantal > positie.aantal:

                print("")
                print(
                    f"Fout: Je hebt slechts "
                    f"{positie.aantal:.2f} stuks {ticker}."
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

            bedrag = aantal * koers

            print("")
            print("Controle verkoop")
            print("------------------------------")
            print(f"Ticker       : {ticker}")
            print(f"Aantal       : {aantal:.2f}")
            print(f"Koers        : €{koers:.2f}")
            print(f"Opbrengst    : €{bedrag:.2f}")
            print("")

            bevestiging = input(
                "Verkoop bevestigen (J/N)? "
            ).strip().upper()

            if bevestiging != "J":

                print("")
                print(
                    "Verkoop geannuleerd."
                )

                continue

            try:
                simulator.verkoop(
                    ticker=ticker,
                    aantal=aantal,
                    koers=koers
                )
                simulator.bewaar_transacties()
                simulator.bewaar_koersen()

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

        ##################################
        # Keuze 6
        ################################## 

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

        ##################################
        # Keuze 7
        ##################################

                )
        elif keuze == "7":

            try:
                simulator.laad_transacties()

                print("")
                print(
                    "Transacties geladen uit transacties.csv"
                )

            except FileNotFoundError:

                print("")
                print(
                    "Fout: transacties.csv bestaat niet."
                )

            except (OSError, ValueError) as fout:

                print("")
                print(
                    f"Fout bij laden: {fout}"

                )

        ##################################
        # Keuze 8
        ##################################

        elif keuze == "8":

            print("")
            print("=== ACTUELE KOERS ===")

            ticker = input(
                "Ticker : "
            ).strip().upper()

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
                simulator.update_koers(
                    ticker=ticker,
                    koers=koers
                )

                simulator.bewaar_koersen()
                                
                print("")
                print(
                    f"Actuele koers van {ticker} "
                    f"ingesteld op €{koers:.2f}"
                )

            except ValueError as fout:

                print("")
                print(
                    f"Fout: {fout}"
                )

        ##################################
        # Keuze 9
        ##################################

        elif keuze == "9":

            simulator.toon_historiek()


        ##################################
        # Keuze 10
        ##################################

        elif keuze == "10":

            simulator.toon_historiek_grafiek()

        ##################################
        # Keuze 11
        ##################################

        elif keuze == "11":
            simulator.toon_winst_verlies_grafiek()


        ##################################
        # Keuze 12
        ##################################

        elif keuze == "12":
            simulator.toon_rendement_grafiek()

    ##################################
    # Keuze 13
    ##################################

        elif keuze == "13":

            print("")
            print("=== SIMULATOR VOLLEDIG RESETTEN ===")
            print("")
            print("Waarschuwing: alle transacties, koersen")
            print("en historiek worden verwijderd.")
            print("")

            bevestiging = input(
                "Ben je zeker? Typ RESET om te bevestigen: "
            ).strip().upper()

            if bevestiging != "RESET":

                print("")
                print("Reset geannuleerd.")
                continue

            bestanden = [
                "transacties.csv",
                "koersen.csv",
                "historiek.csv"
            ]

            for bestandsnaam in bestanden:

                if os.path.exists(bestandsnaam):
                    os.remove(bestandsnaam)

            print("")
            print("Simulator volledig gereset.")
            print("Start het programma opnieuw.")
            break
































       ##################################
        # Keuze 0
       ##################################

        elif keuze == "0":
        
            try:
                simulator.bewaar_transacties()
                simulator.bewaar_koersen()
                simulator.bewaar_historiek()

                print("")
                print(
                    "Transacties automatisch opgeslagen."
                )

            except OSError as fout:

                print("")
                print(
                    f"Fout bij automatisch bewaren: {fout}"
                )

            break

        else:

            print("")
            print("Ongeldige keuze.")

    logger.info(
        "Programma beëindigd"
    )

if __name__ == "__main__":
    main()