"""The SVG Map"""
from twisted.python.util import sibpath

from zope.interface import implements

from nevow import athena, loaders, tags as T

from webby import iwebby, RESOURCE

class BackgroundImage(athena.LiveElement):
    ## jsClass = u'SVGMap.BackgroundImage'
    docFactory = loaders.xmlfile(RESOURCE('elements/BackgroundImage'))
    def __init__(self, channel, *a, **kw):
        super(BackgroundImage, self).__init__(*a, **kw)
        self.channel = channel

    def imageLiveElement(self, req, tag):
        ch = self.channel
        href = u'/files/%s' % (ch.background.md5,)
        obscurementHref = u'/files/%s' % (ch.obscurement.md5,)
        tag.fillSlots('width', ch.background.width)
        tag.fillSlots('height', ch.background.height)
        tag.fillSlots('href', href)
        tag.fillSlots('obscurementHref', obscurementHref)
        return tag(render=T.directive("liveElement"))

    athena.renderer(imageLiveElement)

class MapWidget(athena.LiveElement):
    implements(iwebby.IMapWidget)
    jsClass = u'SVGMap.MapWidget'
    docFactory = loaders.xmlfile(RESOURCE('elements/MapWidget'))
    def __init__(self, channel, chatEntry, *a, **kw):
        super(MapWidget, self).__init__(*a, **kw)
        self.channel = channel
        self.chatEntry = chatEntry

    def setMapBackgroundFromChannel(self):
        """
        Create a new BackgroundImage widget and send it to the channel.
        """
        image = BackgroundImage(self.channel)
        image.setFragmentParent(self)
        return self.callRemote("setMapBackground", image)

    def updateObscurementFromChannel(self):
        """
        Just send a new md5key for the obscurement, which the client-side
        widget will use to reset the background.
        """
        return self.callRemote("updateObscurement", self.channel.obscurement.md5)

    def sendCommand(self, command):
        return self.chatEntry.chatMessage(command)

    athena.expose(sendCommand)
