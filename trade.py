from analyze_data import (
    SECURITIES,
    OFFERS,
    MONEY as money,
)


def decide_if_trade():
    # invoke after every operations
    decide_if_trade.counter += 1

    available_money = 50000 + money

    bond_request = trade_BOND(50000)
    if bond_request:
        price, amount = bond_request
        return "BOND", price, amount

decide_if_trade.counter = 0


def trade_BOND(price_limit):
    bond = SECURITIES['BOND']

    if bond.our_count_waiting == 0:
        if bond.our_count > 0:
            # sell
            price = 1001
            amount = bond.our_count
            amount = -amount
        elif bond.our_count == 0:
            # buy
            price = 999
            amount = price_limit / price
        else:
            AssertionError('value < 0 ?')
        return price, amount
