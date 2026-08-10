from modules.logger import logger
from modules.simulator import BeursSimulator
from modules.etf import ETF
from modules.turbo import Turbo

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
    print("14 - Turbo kopen")
    print("15 - Turbo verkopen")
    print("16 - Onderliggende koers Turbo wijzigen")
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
        # Keuze 14
        # TURBO KOPEN
        ##################################

        elif keuze == "14":

            print("")
            print("=== TURBO KOPEN ===")

            ticker = input(
                "Ticker   : "
            ).strip().upper()

            if not ticker:

                print("")
                print("Fout: Ticker mag niet leeg zijn.")
                continue

            naam = input(
                "Naam     : "
            ).strip()

            if not naam:

                print("")
                print("Fout: Naam mag niet leeg zijn.")
                continue

            soort = input(
                "Soort (LONG/SHORT) : "
            ).strip().upper()

            if soort not in ("LONG", "SHORT"):

                print("")
                print(
                    "Fout: Soort moet LONG of SHORT zijn."
                )
                continue

            try:

                stoploss = float(
                    input(
                        "Stoploss : "
                    ).replace(",", ".")
                )

                onderliggende_koers = float(
                    input(
                        "Onderliggende koers : "
                    ).replace(",", ".")
                )

                hefboom = float(
                    input(
                        "Hefboom  : "
                    ).replace(",", ".")
                )

                aantal = float(
                    input(
                        "Aantal   : "
                    ).replace(",", ".")
                )

                koers = float(
                    input(
                        "Turbo koers : "
                    ).replace(",", ".")
                )

            except ValueError:

                print("")
                print(
                    "Fout: Stoploss, hefboom, aantal "
                    "en koers moeten getallen zijn."
                )
                continue

            if stoploss <= 0:

                print("")
                print(
                    "Fout: Stoploss moet groter zijn dan nul."
                )
                continue

            if onderliggende_koers <= 0:

                print("")
                print(
                    "Fout: Onderliggende koers "
                    "moet groter zijn dan nul."
                )
                continue

            if hefboom <= 0:

                print("")
                print(
                    "Fout: Hefboom moet groter zijn dan nul."
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
                    "Fout: Turbo koers moet groter zijn dan nul."
                )
                continue

            bedrag = aantal * koers

            if bedrag > simulator.portefeuille.cash:

                print("")
                print("Fout: Onvoldoende cash.")

                print(
                    f"Beschikbaar : "
                    f"€{simulator.portefeuille.cash:.2f}"
                )

                print(
                    f"Nodig       : €{bedrag:.2f}"
                )

                continue

            print("")
            print("Controle aankoop")
            print("------------------------------")
            print(f"Ticker               : {ticker}")
            print(f"Naam                 : {naam}")
            print(f"Soort                : {soort}")
            print(f"Stoploss             : {stoploss:.2f}")
            print(
                f"Onderliggende koers  : "
                f"{onderliggende_koers:.2f}"
            )
            print(f"Hefboom              : {hefboom:.2f}x")
            print(f"Aantal               : {aantal:.2f}")
            print(f"Turbo koers          : €{koers:.2f}")
            print(f"Totaalbedrag         : €{bedrag:.2f}")

            try:

                turbo = Turbo(
                    ticker=ticker,
                    naam=naam,
                    soort=soort,
                    stoploss=stoploss,
                    hefboom=hefboom,
                    onderliggende_koers=onderliggende_koers
                )

                afstand = turbo.afstand_tot_stoploss()
                risico = turbo.risicoklasse()

                print("")
                print("Risicoanalyse turbo")
                print("------------------------------")
                print(
                    f"Afstand tot stoploss : {afstand:.2f}%"
                )
                print(
                    f"Risicoklasse         : {risico}"
                )

                if risico == "HOOG RISICO":

                    print(
                        "WAARSCHUWING: deze turbo heeft een hoog risico."
                    )

                print("")

                bevestiging = input(
                    "Aankoop bevestigen (J/N)? "
                ).strip().upper()

                if bevestiging != "J":

                    print("")
                    print("Aankoop geannuleerd.")
                    continue

                simulator.koop(
                    positie=turbo,
                    aantal=aantal,
                    koers=koers
                )

                simulator.bewaar_transacties()
                simulator.bewaar_koersen()

                print("")
                print(
                    f"Turbo aankoop uitgevoerd: "
                    f"{aantal:.2f} {ticker} "
                    f"aan €{koers:.2f}"
                )

            except ValueError as fout:

                print("")
                print(
                    f"Fout: {fout}"
                )

        ##################################
        # Keuze 15
        # TURBO VERKOPEN
        ##################################

        elif keuze == "15":

            print("")
            print("=== TURBO VERKOPEN ===")

            ticker = input(
                "Ticker : "
            ).strip().upper()

            positie = simulator.portefeuille.zoek_positie(
                ticker
            )

            if positie is None:

                print("")
                print(
                    f"Fout: Positie {ticker} bestaat niet."
                )
                continue

            if positie.__class__.__name__ != "Turbo":

                print("")
                print(
                    f"Fout: {ticker} is geen Turbo."
                )
                continue

            print("")
            print(
                f"Beschikbaar: "
                f"{positie.aantal:.2f} stuks {ticker}"
            )

            try:

                aantal = float(
                    input(
                        "Aantal : "
                    ).replace(",", ".")
                )

                koers = float(
                    input(
                        "Koers  : "
                    ).replace(",", ".")
                )

            except ValueError:

                print("")
                print(
                    "Fout: Aantal en koers moeten getallen zijn."
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

            if aantal > positie.aantal:

                print("")
                print(
                    "Fout: Je kunt niet meer verkopen "
                    "dan je bezit."
                )
                continue

            opbrengst = aantal * koers

            print("")
            print("Controle verkoop")
            print("------------------------------")
            print(f"Ticker       : {ticker}")
            print(f"Soort        : {positie.soort}")
            print(f"Stoploss     : {positie.stoploss:.2f}")
            print(f"Hefboom      : {positie.hefboom:.2f}x")
            print(f"Aantal       : {aantal:.2f}")
            print(f"Koers        : €{koers:.2f}")
            print(f"Opbrengst    : €{opbrengst:.2f}")
            print("")

            bevestiging = input(
                "Verkoop bevestigen (J/N)? "
            ).strip().upper()

            if bevestiging != "J":

                print("")
                print("Verkoop geannuleerd.")
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
                    f"Turbo verkoop uitgevoerd: "
                    f"{aantal:.2f} {ticker} "
                    f"aan €{koers:.2f}"
                )

            except ValueError as fout:

                print("")
                print(
                    f"Fout: {fout}"
                )

        ##################################
        # Keuze 16
        # ONDERLIGGENDE KOERS TURBO
        ##################################

        elif keuze == "16":

            print("")
            print("=== ONDERLIGGENDE KOERS TURBO ===")

            ticker = input(
                "Ticker : "
            ).strip().upper()

            positie = simulator.portefeuille.zoek_positie(
                ticker
            )

            if positie is None:

                print("")
                print(
                    f"Fout: Positie {ticker} bestaat niet."
                )
                continue

            if positie.__class__.__name__ != "Turbo":

                print("")
                print(
                    f"Fout: {ticker} is geen Turbo."
                )
                continue

            print("")
            print(
                f"Huidige onderliggende koers : "
                f"{positie.onderliggende_koers:.2f}"
            )

            print(
                f"Stoploss                    : "
                f"{positie.stoploss:.2f}"
            )

            try:

                nieuwe_koers = float(
                    input(
                        "Nieuwe onderliggende koers : "
                    ).replace(",", ".")
                )

            except ValueError:

                print("")
                print(
                    "Fout: Koers moet een getal zijn."
                )
                continue

            if nieuwe_koers <= 0:

                print("")
                print(
                    "Fout: Koers moet groter zijn dan nul."
                )
                continue

            positie.onderliggende_koers = nieuwe_koers

            print("")
            print(
                f"Onderliggende koers van {ticker} "
                f"ingesteld op {nieuwe_koers:.2f}"
            )

            print(
                f"Afstand tot stoploss: "
                f"{positie.afstand_tot_stoploss():.2f}%"
            )

            if positie.stoploss_waarschuwing():

                print("")
                print(
                    "WAARSCHUWING: STOPLOSS DICHTBIJ!"
                )


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