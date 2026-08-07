from modules.etf import ETF
from modules.portefeuille import Portefeuille


def test_koop() -> None:

    portefeuille = Portefeuille(
        10000.00
    )

    iwda = ETF(
        "IWDA",
        "iShares Core MSCI World"
    )

    portefeuille.koop(
        positie=iwda,
        aantal=40,
        koers=124.20
    )

    print("")
    print("=== TEST KOOP ===")

    print(
        f"Cash : €{portefeuille.cash:.2f}"
    )

    print(
        f"Aantal posities : "
        f"{portefeuille.aantal_posities()}"
    )

    positie = portefeuille.zoek_positie(
        "IWDA"
    )

    print(
        f"Aantal IWDA : {positie.aantal}"
    )

    print(
        f"Gemiddelde koers : "
        f"€{positie.gemiddelde_koers:.2f}"
    )


if __name__ == "__main__":
    test_koop()