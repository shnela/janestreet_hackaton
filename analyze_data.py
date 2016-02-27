class Security:
    def __init__(self, name):
        self.name = name

        # all avakuable on the beginning
        self.volume = -1
        self.available = -1
        # our
        self.bought = -1
        self.value_our = -1

        # [price] -> amount
        self.buy_offers = {}
        self.sell_offers = {}

securities_names = [
    "BOND",
    "VALBZ",
    "VALE",
    "GS",
    "MS",
    "WFC",
    "XLF",
]

def book(line):
    splitted_line = line.split()
    stock_name = splitted_line[0]
    action = splitted_line[1]
    data = splitted_line[2:]

    buy_dict = {}
    sell_dict = {}
    state = None
    for entry in data:
        


SECURITIES = [Security(name) for name in securities_names]


def