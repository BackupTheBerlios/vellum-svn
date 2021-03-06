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
import yaml
from dispatch import dispatcher

# local imports
from fs import fs
from models import box, New, Drop, BiDict, loader
from uuid import uuid


model_registry = BiDict()



class NetClient(pb.Referenceable):
    def __init__(self, deferred, username, ):
        self.deferred = deferred
        self.pbfactory = pb.PBClientFactory()
        self.username = username
        self.remote_models = model_registry

    def remote_serverDisconnect(self, message):
        log.msg("DISCONNECTED: %s" % (message,))
        self.pbfactory.disconnect()
        self.deferred.callback(None)

    def remote_receiveNewModel(self,
                               sender,
                               type,
                               object_id,):
        """Called by the avatar to notify that a new object 
        has appeared on the map.
        Notifies the dispatch mechanism.
        """
        print 'received propagated model', object_id
        model = loader.typeByName(type)()
        self.remote_models[model] = object_id
        dispatcher.send(signal=New,
                        sender='remote',
                        model=model)
        model.present()

    def remote_receiveDropModel(self,
                                sender,
                                object_id,):
        """Called by the avatar to notify that an object 
        on the map needs to go away.
        Notifies the dispatch mechanism.
        """
        print 'received propagated drop of model', object_id
        model = self.remote_models[object_id]
        dispatcher.send(signal=Drop,
                        sender='remote',
                        model=model)
        del self.remote_models[object_id]

    def remote_receivePropertyChange(self, 
                                     sender, 
                                     object_id, 
                                     property, 
                                     old, 
                                     value):
        """Called by the avatar to notify that an object has moved, 
        changed colors, etc.
        Notifies the dispatch mechanism.
        """
        model = self.remote_models[object_id]
        dispatcher.send(signal=model, 
                        sender='remote', 
                        property=property, 
                        old=old, 
                        value=value)


    def receiveNewModel(self, sender, model):
        """Called by dispatch mechanism in response to an object being
        created.  Notifies the remote avatar that this has happened.
        """
        if sender != 'remote':
            id = uuid()
            self.remote_models[model] = id
            print 'sending model', id
            self.avatar.callRemote('receiveNewModel',
                                   sender=sender,
                                   type=model.__class__.__name__,
                                   object_id=id)

    def receiveDropModel(self, sender, model):
        """Called by dispatch mechanism in response to an object being
        dropped.  Notifies the remote avatar that this has happened.
        """
        if sender != 'remote':
            id = self.remote_models[model]
            print 'proclaiming removal of', id
            self.avatar.callRemote('receiveDropModel',
                                   sender=sender,
                                   object_id=id)
            del self.remote_models[id]

    def receivePropertyChange(self, 
                              signal, 
                              sender, 
                              property, 
                              old, 
                              value):
        """Called by dispatch mechanism in response to an object property
        changing.  Notifies the remote avatar that this has happened.
        """
        model = signal
        # this is only meant to handle explicit property changes in the gui.
        # It does not re-dispatch changes coming from the network, nor does
        # it dispatch implicit changes made by moving the endpoint of a
        # connector.
        if sender not in ['remote', 'connector', 'presenting']:
            id = self.remote_models[model]
            self.avatar.callRemote('receivePropertyChange', 
                                   object_id=id,
                                   sender=sender,
                                   property=property, 
                                   old=old, 
                                   value=value)

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
        d. addCallback(lambda _: self.avatar.callRemote('getGameState'))
        d.  addCallback(self.gotGame)
        d.addErrback(lambda reason: log.err(reason))
        return d

    def gotGame(self, data):
        for model_data, id in data:
            # create model objects from the yaml received
            model = loader.fromDict(model_data)
            self.remote_models[model] = id

            # and alert the gui and other listeners that models are 
            # alive and kicking.
            dispatcher.send(signal=New, sender='remote', model=model)

            # start telling the gui about the received object
            model.present()


class Gameboy(pb.Avatar):
    def __init__(self, username, mind, models):
        """username - the key for this avatar, user's login id
        mind - a reference to the client so I can push events to my client
        models - the realm's mapping of model:uuid's, a BiDict
        """
        self.mind = mind
        self.username = username
        self.models = models

    def perspective_getGameState(self):
        """Called by the client to request the initial game state at the
        point when the client connects.
        Notifies the dispatch mechanism.
        """
        ret = []
        for id, model in self.models.items(keytype=type('')):
            ret.append((model.dictify(), id))
        return ret

    def perspective_receiveNewModel(self,
                                    sender,
                                    type,
                                    object_id,):
        """Called by the client to notify that a new object has 
        appeared.
        Notifies the dispatch mechanism.
        """
        print 'received and adding model', object_id
        model = loader.typeByName(type)()
        self.models[model] = object_id
        dispatcher.send(signal=New,
                        sender=self.username,
                        model=model)

    def perspective_receiveDropModel(self, 
                                     sender, 
                                     object_id,):
        """Called by the client to notify that an object needs 
        to go away.
        Notifies the dispatch mechanism.
        """
        print 'got proclamation of model removal', object_id
        model = self.models[object_id]
        dispatcher.send(signal=Drop,
                        sender=self.username,
                        model=model)
        del self.models[object_id]

    def perspective_receivePropertyChange(self, 
                                          sender, 
                                          object_id, 
                                          property,
                                          old, 
                                          value):
        """Called by the client to notify that an object property 
        has changed.
        Notifies the dispatch mechanism.
        """
        model = self.models[object_id]
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
            id = self.models[model]
            print 'propagating model', id
            self.mind.callRemote('receiveNewModel',
                    sender='avatar',
                    type=model.__class__.__name__,
                    object_id=id,) 

    def receiveDropModel(self, sender, model):
        """Called by the dispatch to notify that an object needs to 
        go away. Notifies all other avatars' clients but this one.
        """
        if sender != self.username:
            id = self.models[model]
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
        """Called by the dispatch to notify that an object property 
        has changed.
        Notifies remote clients of all other avatars but this one.
        """
        model = signal
        if sender != self.username:
            id = self.models[model]
            self.mind.callRemote('receivePropertyChange', 
                    object_id=id,
                    sender='avatar',
                    property=property,
                    old=old,
                    value=value,
                    )



class GameRealm:
    interface.implements(portal.IRealm)

    def saveGame(self):
        # FIXME - to file
        for id, model in self.models.items(keytype=type('')):
            print yaml.dump({id: model.dictify()})


    def loadSavedGame(self):
        loaded = yaml.loadFile(fs.saved).next()
        for id, data in loaded.items():
            model = loader.fromDict(data)
            self.models[model] = id
            dispatcher.send(signal=New, sender='realm', model=model)
            for prop, value in data.items():
                if prop == 'TYPE':
                    continue
                dispatcher.send(signal=model, 
                                sender='realm', 
                                property=prop,
                                old=None, 
                                value=value)

    def __init__(self):
        self.avatars = {}
        self.models = model_registry
        self.loadSavedGame()
        self.saveGame() # FIXME - for testing porpoises

        

    def requestAvatar(self, username, mind, *interfaces):
        if pb.IPerspective not in interfaces:
            raise NotImplementedError
        if username in self.avatars:
            replaced = self.avatars[username]
            d = replaced.mind.callRemote('serverDisconnect', 
                                         'replaced by new login')
            d.addErrback(lambda f: None)
            del self.avatars[username]
            del replaced
            log.msg('Avatar %s replaced by new login' % (username,))


        avatar = Gameboy(username, mind, self.models)
        self.avatars[username] = avatar
        box.registerObserver(avatar)
        def dc():
            log.msg('Bye-bye, %s' % (avatar.username,))
            del self.avatars[avatar.username]
            box.unregisterObserver(avatar)
        return (pb.IPerspective, avatar, dc,)


def createPortal():
    c = checkers.FilePasswordDB(fs.passwords, 
                                caseSensitive=False, 
                                )
    gameportal = portal.Portal(GameRealm())
    gameportal.registerChecker(c, )
    return gameportal

