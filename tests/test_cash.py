from modules.portefeuille import Portefeuille


def test_cash() -> None:

    portefeuille = Portefeuille(
        10000.00
    )

    portefeuille.boek_af(
        2500.00
    )

    print("")
    print("=== TEST CASH ===")
    print(
        f"Cash na afboeking: "
        f"€{portefeuille.cash:.2f}"
    )

    portefeuille.boek_bij(
        500.00
    )

    print(
        f"Cash na bijboeking: "
        f"€{portefeuille.cash:.2f}"
    )


if __name__ == "__main__":
    test_cash()