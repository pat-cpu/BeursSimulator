from pathlib import Path

# ==============================
# PROJECTMAP
# ==============================

PROJECTMAP = Path(__file__).resolve().parent.parent

# ==============================
# MAPPEN
# ==============================

DATA = PROJECTMAP / "data"
LOGS = PROJECTMAP / "logs"
BACKUP = PROJECTMAP / "backup"

# ==============================
# BESTANDEN
# ==============================

TRANSACTIES = DATA / "transacties.xlsx"
HISTORIEK = DATA / "historiek.csv"
PORTEFEUILLE = DATA / "portefeuille.json"

# ==============================
# INSTELLINGEN
# ==============================

STARTKAPITAAL = 10000

VALUTA = "EUR"

VERSIE = "1.0"