"""
Elements for constructing a window interface.


========================================
Flexible Enclosure (dumb window) Element
========================================

Use one of these for slightly window-like appearance and behavior around a
widget.

Has no callRemotes, but it supports inheritance so you can do things like
notify the iconified window when something on the server generates an event.
(These callRemotes may be added in the future.)

>>> Enclosure(windowTitle="My Window", userClass="someWindowOfMine")

The "userClass" init arg will be inserted into the 'class' attribute of the
node.


===========================
Scrolling Text Area Element
===========================

Use one of these for a console-like text area.

Supports callRemotes for:

    appendTo(content) -> a single, XHTML-namespaced node to add to the widget

"""

from twisted.python.util import sibpath

from nevow import loaders, athena

RESOURCE = lambda f: sibpath(__file__, f)

class Enclosure(athena.LiveElement):
    jsClass = u"Windowing.Enclosure"
    docFactory = loaders.xmlfile(RESOURCE('elements/Enclosure'))
    def __init__(self, windowTitle='~', userClass='', *a, **kw):
        super(Enclosure, self).__init__(*a, **kw)
        self.windowTitleStan = windowTitle
        self.userClassStan = userClass

    def enclosedRegion(self, request, tag):
        return tag['']
    athena.renderer(enclosedRegion)

    def userClass(self, request, tag):
        tag.fillSlots('userClass', self.userClassStan)
        return tag
    athena.renderer(userClass)

    def windowTitle(self, request, tag):
        tag.fillSlots('windowTitle', self.windowTitleStan)
        return tag
    athena.renderer(windowTitle)



class TextArea(athena.LiveElement):
    """A scrollable widget that displays mostly lines of text."""
    jsClass = u"Windowing.TextArea"
    docFactory = loaders.xmlfile(RESOURCE('elements/TextArea'))
    widgetArgs = None

    def printClean(self, message):
        message = flattenMessageString(message)
        return self.callRemote('appendTo', message)

    def setInitialArguments(self, *a, **kw): # FIXME - raped from tabs.py
        assert len(kw) == 0, "Cannot pass keyword arguments to a Widget"
        self.widgetArgs = a

    def getInitialArguments(self): # FIXME - raped from tabs.py
        args = ()
        if self.widgetArgs is not None:
            args = self.widgetArgs

        return args
