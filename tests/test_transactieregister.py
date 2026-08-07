from modules.etf import ETF
from modules.portefeuille import Portefeuille
from modules.transactieregister import TransactieRegister

def test_transactieregister() -> None:

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

    portefeuille.koop(
        positie=iwda,
        aantal=20,
        koers=120.00
    )

    portefeuille.verkoop(
        ticker="IWDA",
        aantal=20,
        koers=130.00
    )

    print("")
    print(
        f"Aantal transacties : "
        f"{portefeuille.transactieregister.aantal()}"
    )

    portefeuille.transactieregister.print_overzicht()

    portefeuille.transactieregister.export_csv(
        "transacties.csv"
    )

    print("")
    print(
        "CSV opgeslagen als transacties.csv"
    )  


if __name__ == "__main__":
    test_transactieregister()