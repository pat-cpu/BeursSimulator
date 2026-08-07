from modules.positie import Positie


class Aandeel(Positie):

    def __init__(self, ticker, naam):
        super().__init__(ticker, naam)