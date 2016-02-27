import sys

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver

from analyze_data import (
    reset_state,
    open,
    close,
    error,
    trade,
    book,
    ack,
    reject,
    fill,
    out,
    SECURITIES,
    MONEY)
from trade import decide_if_trade


class Client(LineReceiver):
    delimiter = b'\n'

    def connectionMade(self):
        reset_state()
        self.message_count = 0
        self.sendLine(b'HELLO DMX')
        print('connected')

    def rawDataReceived(self, data):
        print('raw data received: ', data)

    def lineReceived(self, line):
        line = line.decode('UTF-8')
        command, args = line.split(' ', 1)
        if command == 'OPEN':
            open(args)
        elif command == 'CLOSE':
            close(args)
        elif command == 'ERROR':
            print(command, args)
            error(args)
        elif command == 'BOOK':
            book(args)
        elif command == 'TRADE':
            trade(args)
        elif command == 'ACK':
            ack(args)
        elif command == 'REJECT':
            print(command, args)
            reject(args)
        elif command == 'FILL':
            print(command, args)
            fill(args)
        elif command == 'OUT':
            out(args)
        elif command == 'HELLO':
            print(command, args)
        else:
            raise AssertionError("No such command. From server.")

        decision = decide_if_trade()
        if decision:
            id, name, price, amount = decision
            assert amount
            arg = 'BUY' if amount > 0 else 'SELL'
            amount = abs(amount)
            command = 'ADD {} {} {} {} {}'.format(id, name, arg, price, amount)
            print('sending:', command)
            self.sendLine(command.encode())

        self.message_count += 1
        if not self.message_count % 100:
            print('\nmoney: {}'.format(MONEY))
            print(SECURITIES['BOND'])
            # for s in SECURITIES.values():
            #     print(s)


class ClientFactory(ReconnectingClientFactory):
    protocol = Client

    def __init__(self):
        self.done = Deferred()

    def startedConnecting(self, connector):
        print('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        print('Lost connection. Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)


def main(reactor):
    # prod: python client.py production 20000
    # test normal: python client.py test-exch-dmx 20000
    # test slow: python client.py test-exch-dmx 20001
    # test empty: python client.py test-exch-dmx 20002
    factory = ClientFactory()
    host = sys.argv[1]
    port = int(sys.argv[2])
    reactor.connectTCP(host, port, factory)
    return factory.done


if __name__ == '__main__':
    task.react(main)
