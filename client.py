import sys

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver


class Client(LineReceiver):
    delimiter = b'\n'

    def connectionMade(self):
        self.sendLine(b'HELLO DMX')
        print('connected')

    def rawDataReceived(self, data):
        print('raw data received: ', data)

    def lineReceived(self, line):
        line = line.decode('UTF-8')
        if line.startswith('X'):
            #funccall


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
