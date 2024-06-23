class TranspositionTable:
    def __init__(self):
        self.d = dict()


    def lookup(self, gs):
        return self.d.get(gs.hash, None)


    def store(self, **data):
        """ Stores an entry into the table """
        entry = data.pop("gs").hash
        self.d[entry] = data