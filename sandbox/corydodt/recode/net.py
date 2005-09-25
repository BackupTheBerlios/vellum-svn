"""The PB scaffolding.
PLEASE BE CAREFUL.
Removing any of the remote_ or perspective_ methods here, or changing any of
their return values, will result in incompatible network changes.  Be aware of
that and try to minimize incompatible network changes.

At some point in the future, there will be a policy about what changes are
allowed in what versions.
"""
from twisted.internet import reactor, defer
from twisted.spread import pb
from twisted.python import log
from twisted.cred import credentials, checkers, portal

from zope import interface
from dispatch import dispatcher

# local imports
from fs import fs
from model import Icon, Box, New, Drop
from uuid import uuid




class NetClient(pb.Referenceable):
    def __init__(self, username, ):
        self.pbfactory = pb.PBClientFactory()
        self.remote_control = None
        self.username = username
        self.remote_models = {}
        self.remote_uuids = {}

    def remote_receivePropertyChange(self, 
                                     object_id, 
                                     sender, 
                                     property, 
                                     old, 
                                     value):
        """Called by the avatar to notify that an object has moved, changed
        colors, etc.
        Notifies the dispatch mechanism.
        """
        model = self.remote_models[object_id]
        dispatcher.send(signal=model, 
                        sender='remote', 
                        property=property, 
                        old=old, 
                        value=value)

    def remote_receiveNewModel(self,
                               object_id,
                               sender,
                               ):
        """Called by the avatar to notify that a new object 
        has appeared on the map.
        Notifies the dispatch mechanism.
        """
        print 'received propagated model', object_id
        model = Icon()
        self.addModel(model, object_id)
        dispatcher.send(signal=New,
                        sender='remote',
                        model=model)

    def remote_receiveDropModel(self,
                               object_id,
                               sender,
                               ):
        """Called by the avatar to notify that an object 
        on the map needs to go away.
        Notifies the dispatch mechanism.
        """
        print 'received propagated drop of model', object_id
        model = self.remote_models[object_id]
        self.removeModel(uuid=object_id)
        dispatcher.send(signal=Drop,
                        sender='remote',
                        model=model)

    def receivePropertyChange(self, signal, sender, property, old, value):
        """Called by dispatch mechanism in response to an object property
        changing.  Notifies the remote avatar that this has happened.
        """
        model = signal
        if sender != 'remote':
            id = self.remote_uuids[model]
            self.avatar.callRemote('receivePropertyChange', 
                                   object_id=id,
                                   sender=sender,
                                   property=property, 
                                   old=old, 
                                   value=value)


    def receiveDropModel(self, sender, model):
        """Called by dispatch mechanism in response to an object being
        dropped.  Notifies the remote avatar that this has happened.
        """
        if sender != 'remote':
            id = self.remote_uuids[model]
            print 'proclaiming removal of', id
            self.avatar.callRemote('receiveDropModel',
                                   sender=sender,
                                   object_id=id)

    def receiveNewModel(self, sender, model):
        """Called by dispatch mechanism in response to an object being
        created.  Notifies the remote avatar that this has happened.
        """
        if sender != 'remote':
            id = uuid()
            self.addModel(model, id)
            print 'sending model', id
            self.avatar.callRemote('receiveNewModel',
                                   sender=sender,
                                   object_id=id)
                                   

    def addModel(self, model, id):
        print 'adding model to known', id
        self.remote_models[id] = model 
        self.remote_uuids[model] = id

    def removeModel(self, model=None, uuid=None):
        assert (model, uuid) != (None, None), \
                "Either model or uuid must be given"
        if uuid is None:
            uuid = self.remote_uuids[model]
        print "removing model with id", uuid
        if model is None:
            model = self.remote_models[uuid]
        del self.remote_uuids[model]
        del self.remote_models[uuid]

    def _cb_connected(self, avatar):
        assert hasattr(avatar, 'callRemote'), 'Not connected: %s' % (avatar,)
        log.msg('connected %s' % (repr(avatar,)))
        self.avatar = avatar
        return avatar


    def connectPB(self, server, port):
        reactor.connectTCP(server, port, self.pbfactory)

        creds = credentials.UsernamePassword(self.username, 'password')

        d = self.pbfactory.login(creds, self)

        d.addCallback(self._cb_connected)
        d. addCallback(lambda _: self.avatar.callRemote('getInitialIcon'))
        d.  addCallback(self.gotIcon)
        d.addErrback(lambda reason: log.err(reason))
        return d

    def gotIcon(self, (data, id)):
        icon = Icon()
        self.addModel(icon, id)
        dispatcher.send(signal=New, sender='remote', model=icon)
        dispatcher.send(signal=icon, 
                        sender='remote', 
                        property='location', 
                        old=None, 
                        value=data)


class Gameboy(pb.Avatar):
    def __init__(self, username, mind, realm):
        self.mind = mind
        self.username = username
        # FIXME - passing in the realm here is probably very unsafe
        self.realm = realm

    def perspective_getInitialIcon(self):
        """Called by the client to request the initial game state at the
        point when the client connects.
        Notifies the dispatch mechanism.
        """
        for id, model in self.realm.models.items():
            pass # FIXME - i know this only picks up the last one
        return model.location, id

    def perspective_receiveNewModel(self,
                                    sender,
                                    object_id,
                                    ):
        """Called by the client to notify that a new object has appeared.
        Notifies the dispatch mechanism.
        """
        icon = Icon()
        print 'received and adding model', object_id
        self.realm.addModel(icon, object_id)
        dispatcher.send(signal=New,
                        sender=self.username,
                        model=icon)

    def perspective_receiveDropModel(self, 
                                     sender, 
                                     object_id,):
        """Called by the client to notify that an object needs to go away.
        Notifies the dispatch mechanism.
        """
        print 'got proclamation of model removal', object_id
        icon = self.realm.models[object_id]
        dispatcher.send(signal=Drop,
                        sender=self.username,
                        model=icon)
        self.realm.removeModel(model=icon)

    def perspective_receivePropertyChange(self, 
                                          object_id, 
                                          sender, 
                                          property,
                                          old, 
                                          value):
        """Called by the client to notify that an object property 
        has changed.
        Notifies the dispatch mechanism.
        """
        model = self.realm.models[object_id]
        dispatcher.send(signal=model, 
                        sender=self.username,
                        property=property,
                        old=old, 
                        value=value)



    def receiveNewModel(self, sender, model):
        """Called by the dispatch to notify that a new object exists.
        Notifies remote clients of all other avatars but this one.
        """
        if sender != self.username:
            id = self.realm.uuids[model]
            print 'propagating model', id
            self.mind.callRemote('receiveNewModel',
                    sender='avatar',
                    object_id=id,
                    )
                    


    def receiveDropModel(self, sender, model):
        """Called by the dispatch to notify that an object needs to go away.
        Notifies remote clients of all other avatars but this one.
        """
        if sender != self.username:
            id = self.realm.uuids[model]
            print 'propagating drop of model', id
            self.mind.callRemote('receiveDropModel',
                    sender='avatar',
                    object_id=id,
                    )

    def receivePropertyChange(self,
                              signal,
                              sender,
                              property,
                              old,
                              value):
        """Called by the dispatch to notify that an object property has
        changed.
        Notifies remote clients of all other avatars but this one.
        """
        if sender != self.username:
            self.mind.callRemote('receivePropertyChange', 
                    object_id=self.realm.uuids[signal],
                    sender='avatar',
                    property=property,
                    old=old,
                    value=value,
                    )



class GameRealm:
    interface.implements(portal.IRealm)
    def __init__(self):
        self.box = Box()

        icon = Icon()
        dispatcher.send(signal=New, sender='realm', model=icon)

        data = eval(file(fs.saved, 'rU').read())
        dispatcher.send(signal=icon, 
                        sender='realm', 
                        property='location',
                        old=None, 
                        value=data)

        self.models = {}
        self.uuids = {}

        id = uuid()
        self.addModel(icon, id)

    def addModel(self, model, uuid):
        print "adding model with id", uuid
        self.models[uuid] = model
        self.uuids[model] = uuid

    def removeModel(self, model=None, uuid=None):
        assert (model, uuid) != (None, None), \
                "Either model or uuid must be given"
        if uuid is None:
            uuid = self.uuids[model]
        print "removing model with id", uuid
        if model is None:
            model = self.models[uuid]
        del self.uuids[model]
        del self.models[uuid]
        

    def requestAvatar(self, username, mind, *interfaces):
        if pb.IPerspective not in interfaces:
            raise NotImplementedError
        avatar = Gameboy(username, mind, self)
        self.box.registerObserver(avatar)
        def dc():
            log.msg('Bye-bye, %s' % (avatar.username,))
            self.box.unregisterObserver(avatar)
        return (pb.IPerspective, avatar, dc,)


def createPortal():
    c = checkers.FilePasswordDB(fs.passwords, 
                                caseSensitive=False, 
                                )
    gameportal = portal.Portal(GameRealm())
    gameportal.registerChecker(c, )
    return gameportal

