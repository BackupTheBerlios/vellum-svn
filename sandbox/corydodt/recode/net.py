from twisted.internet import reactor, defer
from twisted.spread import pb
from twisted.python import log
from twisted.cred import credentials

from dispatch import dispatcher

import fs
from model import Icon, New


class Receiver(pb.Referenceable):
    def __init__(self, remote_models):
        self.remote_models = remote_models
    def remote_receivePropertyChange(self, 
                                     object_id, 
                                     sender, 
                                     property, 
                                     old, 
                                     value):
        model = self.remote_models[object_id]
        dispatcher.send(signal=model, 
                        sender='remote', 
                        property=property, 
                        old=old, 
                        value=value)


class NetClient:
    def __init__(self, username, ):
        self.pbfactory = pb.PBClientFactory()
        self.remote_control = None
        self.username = username
        self.remote_models = {}
        self.remote_uuids = {}

    def receivePropertyChange(self, signal, sender, property, old, value):
        model = signal
        print sender
        if sender != 'remote':
            self.avatar.callRemote('receivePropertyChange', 
                                   object_id=self.remote_uuids[model],
                                   sender=sender,
                                   property=property, 
                                   old=old, 
                                   value=value)


    def receiveDropModel(self, sender, model):
        FIXME 

    def receiveNewModel(self, sender, model):
        pass

    def _cb_connected(self, avatar):
        assert hasattr(avatar, 'callRemote'), 'Not connected: %s' % (avatar,)
        log.msg('connected %s' % (repr(avatar,)))
        self.avatar = avatar
        return avatar


    def connectPB(self, server, port):
        reactor.connectTCP(server, port, self.pbfactory)

        creds = credentials.UsernamePassword(self.username, 'X')

        d = self.pbfactory.login(creds, Receiver(self.remote_models))

        d.addCallback(self._cb_connected)
        d. addCallback(lambda _: self.avatar.callRemote('getInitialIcon'))
        d.  addCallback(self.gotIcon)
        d.addErrback(lambda reason: log.err(reason))
        return d

    def gotIcon(self, (data, id)):
        icon = Icon()
        self.remote_models[id] = icon
        self.remote_uuids[icon] = id
        dispatcher.send(signal=New, sender='remote', model=icon)
        dispatcher.send(signal=icon, sender='remote', property='location', 
                old=None, value=data)

