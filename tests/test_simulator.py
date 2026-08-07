from modules.etf import ETF
from modules.simulator import BeursSimulator


def test_simulator() -> None:

    simulator = BeursSimulator()

    iwda = ETF(
        "IWDA",
        "iShares Core MSCI World"
    )

    simulator.portefeuille.koop(
        positie=iwda,
        aantal=10,
        koers=125.00
    )

    print("")
    print("=== TEST SIMULATOR ===")

    print(
        f"Cash : €{simulator.portefeuille.cash:.2f}"
    )

    print(
        f"Aantal posities : "
        f"{simulator.portefeuille.aantal_posities()}"
    )

    print(
        f"Aantal transacties : "
        f"{simulator.transactieregister.aantal()}"
    )

    print(
        "Zelfde register :",
        simulator.transactieregister
        is simulator.portefeuille.transactieregister
    )


if __name__ == "__main__":
    test_simulator()