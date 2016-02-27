class Security:
    def __init__(self, name):
        self.name = name

        # all avakuable on the beginning
        self.volume = None
        self.available = None
        # our
        self.bought = None
        self.value_our = None

        # avg between max_buy and min_sell propositions
        self.center_price = None

        # [price] -> amount
        self.buy_offers = {}
        self.sell_offers = {}


class Offer:
    SENT = 'SENT'
    ACK = 'ACK'
    REJECT = 'REJECT'

    def __init__(self, id, symbol, dir, price, size, status=SENT):
        if dir not in ('BUY', 'SELL'):
            raise ValueError('dir not in (SELL, BUY)')

        self.id = id
        self.symbol = symbol
        self.dir = dir
        self.price = price
        self.size = size
        self.status = status  # possible: SENT, ACK, REJECT


# [id] -> offer
OFFERS = {}


securities_names = [
    "BOND",
    "VALBZ",
    "VALE",
    "GS",
    "MS",
    "WFC",
    "XLF",
]

SECURITIES = {name: Security(name) for name in securities_names}


def book(line):
    """
    update information about pending offers
    extract avg price min/max TODO - improve to take wider range of offers into consideration
    """
    splitted_line = line.split()
    stock_name = splitted_line[0]
    data = splitted_line[2:] # omit BUY string

    buy_dict = {}
    sell_dict = {}
    buy_data = True # buy
    max_buy_price = None
    min_sell_price = None
    for entry in data:
        if entry == 'SELL':
            buy_data = False
            continue
        price, volume = entry.split(':')
        if buy_data:
            buy_dict[price] = volume
            if not max_buy_price:
                max_buy_price = price
            max_buy_price = max(max_buy_price, price)
        else:
            sell_dict[price] = volume
            if not min_sell_price:
                min_sell_price = price
            min_sell_price = min(min_sell_price, price)

    center_price = max_buy_price + ((min_sell_price - max_buy_price) / 2) if max_buy_price and min_sell_price else None

    global SECURITIES
    SECURITIES[stock_name].buy_offers = buy_dict
    SECURITIES[stock_name].sell_offers = sell_dict
    SECURITIES[stock_name].center_price = center_price


def ack(line):
    offer_id = int(line.split()[1])

    global OFFERS
    OFFERS[offer_id].status = Offer.ACK


def reject(line):
    _, offer_id, message = line.split()
    offer_id = int(offer_id)

    global OFFERS
    OFFERS[offer_id].status = Offer.REJECT
