# global variables
OFFERS = {}  # id -> offer
SECURITIES = {}  # name -> offer
MONEY = 0


class Security:
    def __init__(self, name):
        self.name = name
        self.is_open = False

        self.our_count_waiting_sell = 0
        self.our_count_waiting_buy = 0
        self.our_count = 0
        # locked if waiting for decisin if Offer is accepted or not
        self.locked = False

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

    def __str__(self):
        return '{}: avg price {}, our_count {}, our_count_waiting_sell {}, our_count_waiting_buy {}'.format(
            self.name, self.avg_transactions_value, self.our_count, self.our_count_waiting_sell, self.our_count_waiting_buy
        )


class Offer:
    SENT = 'SENT'
    ACK = 'ACK'
    REJECT = 'REJECT'
    BUY = 'BUY'
    SELL = 'SELL'
    id = 0

    def __init__(self, symbol, dir, price, size, status=SENT):
        if dir not in ('BUY', 'SELL'):
            raise ValueError('dir not in (SELL, BUY)')

        self.id = Offer.get_id()
        self.symbol = symbol
        self.dir = dir
        self.price = price
        self.size = size
        assert(size >= 0)
        self.status = status  # possible: SENT, ACK, REJECT
        self.left = size
        self.out = False

        security = SECURITIES[self.symbol]
        security.locked = True

    def change_status(self, status):
        if status not in (self.ACK, self.REJECT):
            raise ValueError('status not ACK OR REJECT')
        self.status = status

        security = SECURITIES[self.symbol]
        security.locked = False

        if status == self.ACK:
            assert(self.size >= 0)
            if self.dir == Offer.SELL:
                security.our_count_waiting_sell += self.size
            elif self.dir == Offer.BUY:
                security.our_count_waiting_buy += self.size

    @staticmethod
    def get_id():
        Offer.id += 1
        return Offer.id


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
    data = splitted_line[2:]  # omit BUY string

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
    offer_id = int(line)

    global OFFERS, SECURITIES
    offer = OFFERS[offer_id]
    offer.change_status(Offer.ACK)


def reject(line):
    splitted_line = line.split()
    offer_id = splitted_line[0]
    message = splitted_line[1:]
    offer_id = int(offer_id)

    global OFFERS
    OFFERS[offer_id].change_status(Offer.REJECT)


def fill(line):
    offer_id, _, _, price, size = line.split()
    offer_id = int(offer_id)
    size = int(size)
    price = int(price)

    global OFFERS, SECURITIES, MONEY
    offer = OFFERS[offer_id]
    offer.left -= size

    security = SECURITIES[offer.symbol]

    if offer.dir == Offer.SELL:
        security.our_count -= size
        security.our_count_waiting_sell -= size
        assert(security.our_count_waiting_sell >= 0)
        MONEY += price
    elif offer.dir == Offer.BUY:
        security.our_count += size
        security.our_count_waiting_buy -= size
        assert(security.our_count_waiting_buy >= 0)
        MONEY -= price


def out(line):
    offer_id = int(line.strip())

    global OFFERS
    OFFERS[offer_id].out = True


def error(line):
    pass
