from analyze_data import (
    SECURITIES,
    OFFERS,
    MONEY as money,
    Offer,
)


def decide_if_trade():
    # invoke after every operations
    decide_if_trade.counter += 1

    the_best_request = trade_XLF()

    if the_best_request:
        symbol, price, amount = the_best_request

        direction = 'BUY' if amount > 0 else 'SELL'
        offer = Offer(symbol, direction, price, abs(amount))
        OFFERS[offer.id] = offer
        return offer.id, "XLF", price, amount


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


def compute_XLF_value():
    values = {
        'BOND': 1000,
        'GS': SECURITIES['GS'].center_price,
        'MS': SECURITIES['MS'].center_price,
        'WFC': SECURITIES['WFC'].center_price,
    }

    return 3 * values['BOND'] + 2 * values['GS'] + 3 * values['MS'] + 2 * values['WFC']


def trade_XLF():
    xlf = SECURITIES['XLF']

    if not xlf.center_price:
        return

    if xlf.is_open and not xlf.locked:
        available_to_buy = 100 - xlf.our_count - xlf.our_count_waiting_buy - xlf.our_count_waiting_sell

        if (xlf.our_count - xlf.our_count_waiting_sell) > 0:
            return xlf.name, xlf.center_price + 1, -xlf.our_count
        elif available_to_buy:
            return xlf.name, xlf.center_price - 1, available_to_buy


def decide_if_convert_XLF():
    xlf = SECURITIES['XLF']

    if compute_XLF_value() > xlf.center_price and xlf.our_count >= 10:
        return xlf.our_count % 10 * 10
