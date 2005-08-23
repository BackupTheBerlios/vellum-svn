#!python
import warnings
warnings.filterwarnings('ignore')


# install must happen first because reactors are magikal
from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor, defer
from twisted.python import log

import sys


# locals
from net import NetClient
from view import BigController, BigView
from fs import fs
from model import Box

def finish(fail, ):
    """This doubles as callback and errback"""
    try:
        if fail is not None:
            log.err(fail)
    finally:
        reactor.stop()

def run(argv = None):
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        username = argv[1]
    else:
        username = None

    d = defer.Deferred()

    box = Box()
    
    netclient = NetClient(username or 'jezebel', )
    bigctl = BigController(d, )
    bigview = BigView(bigctl)

    box.registerObserver(netclient)
    box.registerObserver(bigctl)

    reactor.callLater(0, netclient.connectPB, 'localhost', 9559)

    d.addCallback(finish, ).addErrback(finish, )

    reactor.run()

if __name__ == '__main__':
    run()

