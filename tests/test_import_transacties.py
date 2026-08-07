from modules.transactieregister import TransactieRegister


def test_import_transacties() -> None:

    register = TransactieRegister()

    register.import_csv(
        "transacties.csv"
    )

    print("")
    print(
        f"Aantal geïmporteerde transacties : "
        f"{register.aantal()}"
    )

    register.print_overzicht()


if __name__ == "__main__":
    test_import_transacties()