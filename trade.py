from analyze_data import (
    SECURITIES,
    OFFERS,
    MONEY as money,
)


def trade():
    # invoke after every operations
    trade.counter += 1

    available_money = 50000 + money

    bond_request = trade_BOND(50000)
    if bond_request:
        price, amount = bond_request[0], bond_request[1]
        return price, amount

trade.counter = 0


def trade_BOND(price_limit):
    bond = SECURITIES['BOND']
    bond_offer = OFFERS['BOND']

    value = 1000
    if bond.our_amount > 0 and bond_offer:
        price = 995
        amount = price_limit / 995
    return price, amount
