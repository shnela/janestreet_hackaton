# global variables
OFFERS = {}
SECURITIES = {}
MONEY = 0


class Security:
    def __init__(self, name):
        self.name = name
        self.is_open = False

        self.our_amount_waiting = 0
        self.our_amount = 0

        # all avakuable on the beginning
        self.volume = None
        self.available = None

        # list of values of last transactions
        self.last_prices = []
        self.avg_transactions_value = None

        # avg between max_buy and min_sell propositions
        self.center_price = None

        # [price] -> amount
        self.buy_offers = {}
        self.sell_offers = {}

    def count_avg_transaction_value(self, n=None):
        values = self.last_prices[-n:] if n else self.last_prices
        self.avg_transactions_value = sum(values) / len(values)
        return self.avg_transactions_value

    def count_center_price(self):
        if not self.buy_offers or not self.sell_offers:
            return

        min_sell_price = min(self.sell_offers.keys())
        max_buy_price = max(self.buy_offers.keys())

        self.center_price = max_buy_price + ((min_sell_price - max_buy_price) / 2)
        return self.center_price


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
        self.left = size
        self.out = False


securities_names = [
    "BOND",
    "VALBZ",
    "VALE",
    "GS",
    "MS",
    "WFC",
    "XLF",
]


def reset_state():
    # [id] -> offer
    global OFFERS
    global SECURITIES
    global MONEY
    OFFERS.clear()
    for name in securities_names:
        SECURITIES[name] = Security(name)
    MONEY = 0


def open(line):
    global SECURITIES
    for symbol in line.split():
        SECURITIES[symbol].is_open = True


def close(line):
    global SECURITIES
    for symbol in line.split():
        SECURITIES[symbol].is_open = False


def trade(line):
    symbol, price, size = line.split()
    price = int(price)
    size = int(size)

    global SECURITIES
    SECURITIES[symbol].last_prices.append(price)


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
    for entry in data:
        if entry == 'SELL':
            buy_data = False
            continue
        price, volume = entry.split(':')
        price = int(price)
        volume = int(volume)
        if buy_data:
            buy_dict[price] = volume
        else:
            sell_dict[price] = volume

    global SECURITIES
    SECURITIES[stock_name].buy_offers = buy_dict
    SECURITIES[stock_name].sell_offers = sell_dict
    SECURITIES[stock_name].count_center_price()


def ack(line):
    offer_id = int(line.split()[1])

    global OFFERS
    OFFERS[offer_id].status = Offer.ACK


def reject(line):
    _, offer_id, message = line.split()
    offer_id = int(offer_id)

    global OFFERS
    OFFERS[offer_id].status = Offer.REJECT


def fill(line):
    _, offer_id, _, _, _, size = line.split()
    offer_id = int(offer_id)
    size = int(size)

    global OFFERS
    OFFERS[offer_id].left -= size


def out(line):
    offer_id = int(line.split()[1])

    global OFFERS
    OFFERS[offer_id].out = True
