"""The PB service of the vellum server.
PLEASE BE CAREFUL.
Removing any of the remote_ methods here, or changing any of their return
values, will result in incompatible network changes.  Be aware of that and
try to minimize incompatible network changes.

At some point in the future, there will be a policy about what changes are
allowed in what versions.
"""
import re

from twisted.spread import pb
from twisted.cred import checkers, portal
from twisted.python import log

from zope import interface

from dispatch import dispatcher

# local imports
from fs import fs
from uuid import uuid
from model import Icon, Box, New


class Gameboy(pb.Avatar):
    def __init__(self, username, mind, realm):
        self.mind = mind
        self.username = username
        # FIXME - passing in the realm here is probably very unsafe
        self.realm = realm

    def perspective_getInitialIcon(self):
        for id, model in self.realm.models.items():
            pass # FIXME - i know this only picks up the last one
        return model.location, id

    def perspective_receivePropertyChange(self, 
                                          object_id, 
                                          sender, 
                                          property,
                                          old, 
                                          value):
        model = self.realm.models[object_id]
        dispatcher.send(signal=model, 
                        sender=self.username,
                        property=property,
                        old=old, 
                        value=value)

    def receivePropertyChange(self,
                              signal,
                              sender,
                              property,
                              old,
                              value):
        """Just echo changes so the rest of the world picks them up"""
        print '%s from %s' % (value, sender)
        if sender != self.username:
            self.mind.callRemote('receivePropertyChange', 
                    object_id=self.realm.uuids[signal],
                    sender='avatar',
                    property=property,
                    old=old,
                    value=value,
                    )

    def receiveNewModel(self, sender, model):
        FIXME

    def receiveDropModel(self, sender, model):
        FIXME



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

        self.addModel(icon, uuid())

    def addModel(self, model, uuid):
        self.models[uuid] = model
        self.uuids[model] = uuid

    def removeModel(self, model=None, uuid=None):
        assert (model, uuid) != (None, None), \
                "Either model or uuid must be given"
        if uuid is None:
            uuid = self.uuids[model]
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
            log.msg('bye bye %s' % (avatar.username,))
            self.box.unregisterObserver(avatar)
        return (pb.IPerspective, avatar, dc,)


c = checkers.InMemoryUsernamePasswordDatabaseDontUse(jezebel='X',
                                                     gm='X',
                                                     )
gameportal = portal.Portal(GameRealm())
gameportal.registerChecker(c)

