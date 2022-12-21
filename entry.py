import time
import QueryGenerator as generateQuery

m2h = lambda num: num//60 if not num%60 else round(num/60, 3)
# convert minutes to hours

class Entry:

    def __init__(self, data, parent):
        self.raw = data
        self.config = parent.config
        self.parent = parent


    def __repr__(self):
        return f"Entry({m2h(self.raw[1])}, '{time.ctime(self.raw[2])}', '{self.raw[3]}', (" + str(self.tags)[1:-1] + "))"


    def __eq__(self, other):
        try: return self.raw[0] == other.raw[0]
        except AttributeError: return False


    @property
    def tags(self):
        lookup = self.config["tags"]
        return [lookup[i] for i, x in enumerate(self.raw[4:]) if x == 1]


    @property
    def hours(self): return m2h(self.raw[1])

    @property
    def date(self): return time.ctime(self.raw[2])

    @property
    def description(self): return self.raw[3]

    @property
    def id(self): return self.raw[0]
