from modules.portefeuille import Portefeuille
from modules.transactieregister import TransactieRegister


def test_opbouwen_portefeuille() -> None:

    register = TransactieRegister()

    register.import_csv(
        "transacties.csv"
    )

    portefeuille = Portefeuille(
        10000.00
    )

    portefeuille.opbouwen_uit_transacties(
        register
    )

    positie = portefeuille.zoek_positie(
        "IWDA"
    )

    print("")
    print("=== OPGEBOUWDE PORTEFEUILLE ===")

    print(
        f"Cash : €{portefeuille.cash:.2f}"
    )

    print(
        f"Aantal posities : "
        f"{portefeuille.aantal_posities()}"
    )

    print(
        f"Aantal IWDA : {positie.aantal}"
    )

    print(
        f"Gemiddelde koers : "
        f"€{positie.gemiddelde_koers:.2f}"
    )


if __name__ == "__main__":
    test_opbouwen_portefeuille()