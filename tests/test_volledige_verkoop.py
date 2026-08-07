from modules.etf import ETF
from modules.portefeuille import Portefeuille


def test_volledige_verkoop() -> None:

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

    portefeuille.verkoop(
        ticker="IWDA",
        aantal=40,
        koers=130.00
    )

    print("")
    print("=== TEST VOLLEDIGE VERKOOP ===")

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
        f"Positie IWDA : {positie}"
    )


if __name__ == "__main__":
    test_volledige_verkoop()