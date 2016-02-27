from analyze_data import (
    SECURITIES,
    OFFERS,
    MONEY as money,
    Offer,
)


def decide_if_trade():
    # invoke after every operations
    decide_if_trade.counter += 1

    available_money = 50000 + money

    bond_request = trade_BOND(50000)
    the_best_request = bond_request

    if the_best_request:
        symbol, price, amount = bond_request

        # TODO @Ulit give me a id
        direction = 'BUY' if amount > 0 else 'SELL'
        offer = Offer(symbol, direction, price, amount)
        OFFERS[offer.id] = offer
        return offer.id, "BOND", price, amount

decide_if_trade.counter = 0


def trade_BOND(price_limit):
    bond = SECURITIES['BOND']

    if bond.is_open and bond.our_count_waiting == 0:
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
        return bond.name, price, amount
