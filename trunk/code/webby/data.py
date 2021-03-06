import sys, os
from decimal import Decimal
from md5 import md5

from twisted.application import service
from twisted.python import log
from twisted.internet import defer

from axiom import store, substore, item, attributes as A

from zope.interface import Interface, implements

from epsilon.extime import Time

from webby import obscurement
from webby.iwebby import IFileObserver

EPOCH = Time.fromPOSIXTimestamp(0)

class DataService(item.Item, service.Service):
    powerupInterfaces = (service.IService,)
    schemaVersion = 1
    smtpFrom = A.text(doc="The email address used as From: in emails")
    smtpServer = A.text(doc="The SMTP server used for outgoing email")

    parent = A.inmemory()
    running = A.inmemory()

    def startService(self):
        log.msg("Starting service %r" % (self, ))

class IArticle(Interface):
    """
    A thing you can put on a map, such as a character or sound effect node
    """


class _ArticleMixin(object):
    implements(IArticle)

    def installOn(self, other):
        other.powerUp(self, IArticle)


class Character(item.Item, _ArticleMixin):
    """A player character or NPC"""
    schemaVersion = 1
    name = A.text(allowNone=False)
    path = A.path(allowNone=False, relative=True)
    top = A.point4decimal()
    left = A.point4decimal()
    scale = A.point4decimal(allowNone=False)


class User(item.Item):
    schemaVersion = 2
    email = A.text(doc="The username used to log in", allowNone=False)
    nick = A.text(doc="The default nick to use in IRC")
    firstname = A.text(doc="The first name of the user")
    lastname = A.text(doc="The last name of the user")
    password = A.text(doc="The password of the user")
    recentChannels = A.text(doc="Channels the user was in most recently",
            default=u'#vellum')
    confirmationKey = A.text(doc="A random number generated to send to the user's email address")
    unconfirmedPassword = A.text(doc="Password is held here until confirmationKey is validated.")
    observers = A.inmemory(doc="List of IFileObservers")

    def activate(self):
        self.observers = []

    def addRecentChannel(self, channelName):
        if self.recentChannels == u'':
            channels = []
        else:
            channels = self.recentChannels.split(u',')

        if channelName not in channels:
            # TODO - clean up duplicates?
            channels.append(unicode(channelName))
            self.recentChannels = u','.join(channels)

    def removeRecentChannel(self, channelName):
        if self.recentChannels == u'':
            channels = []
        else:
            channels = self.recentChannels.split(u',')

        if channelName in channels:
            channels.remove(channelName)
            self.recentChannels = u','.join(channels)

    def fileAdded(self, fileitem):
        assert fileitem.user is self
        r = []
        for o in self.observers:
            r.append(IFileObserver(o).fileAdded(fileitem))
        return defer.DeferredList(r, False, True)

    def fileRemoved(self, fileitem):
        assert fileitem.user is self
        r = []
        for o in self.observers:
            r.append(IFileObserver(o).fileRemoved(fileitem))
        return defer.DeferredList(r, False, True)

    def fileModified(self, fileitem):
        assert fileitem.user is self
        r = []
        for o in self.observers:
            r.append(IFileObserver(o).fileModified(fileitem))
        return defer.DeferredList(r, False, True)

    def addObserver(self, observer):
        self.observers.append(observer)

    def removeObserver(self, observer):
        self.observers.remove(observer)

class FileMeta(item.Item):
    """A file that has been uploaded."""
    schemaVersion = 1
    data = A.reference(doc="The FileData item that holds this file's data")
    thumbnail = A.reference(doc="The FileData item that holds the image thumbnail, if any")
    filename = A.text(doc="The basename of the file")
    mimeType = A.text(doc="The mime-type of the file")
    md5 = A.text(doc="The md5 hash of the file data")
    user = A.reference(doc="The User item who uploaded (owns?) the file")
    width = A.integer(doc="The width in pixels of the image, if an image")
    height = A.integer(doc="The height in pixels of the image, if an image")


class FileData(item.Item):
    schemaVersion = 1
    data = A.bytes(doc="The bytes in the file")

    def __repr__(self):
        return '<FileData @%x>' % (id(self),)


class Channel(item.Item):
    schemaVersion = 1
    name = A.text(doc="Name of the channel")
    topic = A.text(doc="What the channel topic is")
    topicAuthor = A.text(doc="Who set the topic")
    topicTime = A.timestamp(doc="When the topic was set", default=EPOCH)
    background = A.reference(doc="Image for the background of the channel map")
    obscurement = A.reference(doc="Image that stores the obscurement overlay")
    gameTime = A.text(doc="A representation of the time in the game session")
    scale100px = A.point4decimal(doc="Distance in meters of 100 map px @ 100% zoom")

    def getBackgroundCommand(self):
        """Return the IRC command to represent the Background"""
        return u"BACKGROUND %s %s" % (self.name, self.background.md5)

    def getDigestedForm(self):
        ret = []
        if self.background:
            ret.append(self.getBackgroundCommand())

        return ret

    def setObscurement(self, bytes):
        def txn():
            ob = FileMeta(store=self.store)
            ob.filename = u'%s_obscurement.png' % (self.name,)
            ob.width = self.background.width
            ob.height = self.background.height
            ob.mimeType = u'image/png'

            ob.data = FileData(store=self.store)
            ob.data.data = bytes

            ob.md5 = unicode(md5(ob.data.data).hexdigest())

            orig = self.obscurement
            self.obscurement = ob

            if orig is not None: 
                orig.deleteFromStore()

        self.store.transact(txn)

    def setBackground(self, fileitem):
        def txn():
            self.background = fileitem
            w = fileitem.width
            h = fileitem.height

            # reset the obscurement every time the background is updated
            self.obscureAll()

        self.store.transact(txn)

    def obscureAll(self):
        if self.background:
            def txn():
                w = self.background.width
                h = self.background.height
                self.setObscurement(obscurement.newBlackImage(w, h))

            self.store.transact(txn)

    def revealAll(self):
        if self.background:
            def txn():
                w = self.background.width
                h = self.background.height
                self.setObscurement(obscurement.newTransparentImage(w, h))

            self.store.transact(txn)
