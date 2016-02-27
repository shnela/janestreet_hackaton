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

    bond_request = trade_BOND(available_money)
    the_best_request = bond_request

    if the_best_request:
        symbol, price, amount = bond_request

        direction = 'BUY' if amount > 0 else 'SELL'
        offer = Offer(symbol, direction, price, amount)
        OFFERS[offer.id] = offer
        return offer.id, "BOND", price, amount

decide_if_trade.counter = 0


def trade_BOND(price_limit):
    bond = SECURITIES['BOND']

    if bond.is_open and not bond.locked and bond.our_count_waiting == 0:
        if bond.our_count > 0:
            # sell
            price = 1001
            amount = bond.our_count - bond.our_count_waiting
            amount = -amount
        elif bond.our_count == 0:
            # buy
            price = 999
            # amount = price_limit // price
            amount = 50000 // price - bond.our_count_waiting
        else:
            raise AssertionError('value < 0 ?')

        return bond.name, price, amount


def trade_VALBZ_VALE(price_limit):
    vale = SECURITIES['VALE']
    valbz = SECURITIES['VALBZ']

    if vale.is_open and vale.our_count_waiting == 0:
        if vale.our_count > 0:
            price = valbz.center_price + 2
            amount = -vale.our_count
        elif vale.our_count == 0:
            price = valbz.center_price - 2
            amount = price_limit // price
        else:
            raise AssertionError('stuff happened')

        return vale.name, price, amount
