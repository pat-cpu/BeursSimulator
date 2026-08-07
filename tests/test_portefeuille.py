from modules.etf import ETF
from modules.portefeuille import Portefeuille


def test_portefeuille():

    portefeuille = Portefeuille()

    iwda = ETF(
        "IWDA",
        "iShares Core MSCI World"
    )

    iwda.koop(
        aantal=40,
        koers=124.20
    )

    portefeuille.voeg_positie_toe(
        iwda
    )

    print("")
    print("=== TEST PORTEFEUILLE ===")
    print(
        f"Ticker: {iwda.ticker}"
    )
    print(
        f"Aantal: {iwda.aantal}"
    )
    print(
        f"Gemiddelde koers: "
        f"€{iwda.gemiddelde_koers:.2f}"
    )
    print(
        f"Aankoopwaarde: "
        f"€{iwda.aankoopwaarde:.2f}"
    )
    print(
        f"Aantal posities: "
        f"{portefeuille.aantal_posities()}"
    )


if __name__ == "__main__":
    test_portefeuille()