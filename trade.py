from analyze_data import (
    SECURITIES,
    OFFERS,
    MONEY as money,
    Offer,
)


def decide_if_trade():
    # invoke after every operations
    decide_if_trade.counter += 1

    the_best_request = trade_BOND()

    if the_best_request:
        symbol, price, amount = the_best_request

        direction = 'BUY' if amount > 0 else 'SELL'
        offer = Offer(symbol, direction, price, abs(amount))
        OFFERS[offer.id] = offer
        return offer.id, "BOND", price, amount

decide_if_trade.counter = 0


def trade_BOND():
    bond = SECURITIES['BOND']

    if bond.is_open and not bond.locked:
        available_to_buy = 100 - bond.our_count - bond.our_count_waiting_buy
        if (bond.our_count - bond.our_count_waiting_sell) > 0:
            return bond.name, 1001, -bond.our_count
        elif available_to_buy:
            return bond.name, 999, available_to_buy


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
