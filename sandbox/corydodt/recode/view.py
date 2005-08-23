from __future__ import division

import gtk
from gtk import gdk


from twisted.python import log
from twisted.internet import reactor

# my windows build of gnomecanvas uses a nonstandard name
try:
    from gnome import canvas as gnomecanvas
except ImportError:
    import gnomecanvas

from dispatch import dispatcher

# vellum imports
from fs import fs



class BigView:
    """All the widgets down to the main window"""
    def __init__(self, controller):
        w = gtk.Window()
        w.show()

        c = self.controller = controller
        c.view = self

        """Put in a canvas"""
        canvas = gnomecanvas.Canvas()
        canvas.set_center_scroll_region(False)

        w.add(canvas)
        canvas.show()

        canvas.connect('button-press-event', 
                       c.on_canvas_button_press_event)
        canvas.connect('button-release-event', 
                       c.on_canvas_button_release_event)
        canvas.connect('motion-notify-event', 
                       c.on_canvas_motion_notify_event)
        w.connect('destroy', c.on_Vellum_destroy)
        self.canvas = canvas

class BigController:
    def __init__(self, deferred):
        self.deferred = deferred

    def receiveNewModel(self, sender, model): 
        receiver = getattr(self, 'new_%s' % (model.__class__.__name__))
        receiver(model)

    def receiveDropModel(self, sender, model): 
        FIXME # no drop actions yet
        receiver = getattr(self, 'drop_%s' % (model.__class__.__name__))
        receiver(model)

    def receivePropertyChange(self, 
                              signal, 
                              sender, 
                              property, 
                              old, 
                              value):
        receiver = getattr(self, 'changed_%s_%s' % (
                signal.__class__.__name__, property))
        receiver(signal, sender, old, value)

    def changed_Icon_location(self, icon, sender, old, (x, y)):
        if old is None: old = (0,0)
        ox, oy = old
        icon.widget.move(x-ox, y-oy)

    def new_Icon(self, icon):
        # clean up icon if necessary
        if getattr(icon, 'widget', None) is not None:
            icon.widget.destroy()
            icon.widget = None

        # make an image
        image = icon.image = gdk.pixbuf_new_from_file(fs.crom)

        # place it on the canvas
        canvas = self.view.canvas
        root = canvas.root()
        corner = icon.location
        if corner is None: corner = (0,0)
        x, y = corner
        if icon.widget is None:
            igroup = root.add("GnomeCanvasGroup", x=x, y=y)
            igroup.add("GnomeCanvasPixbuf",
                     pixbuf=image,
                     x=0, y=0)


            igroup.connect('event', self.on_icon_event, icon)
            icon.widget = igroup


    def on_icon_event(self, widget, event, icon):
        type = event.type.value_name.lower()
        handler = getattr(self, 'on_icon_%s' % (type,), None)
        if handler is not None:
            return handler(widget, event, icon)

    def on_icon_gdk_button_press(self, widget, event, icon):
        icon.grabbed = True

    def on_icon_gdk_button_release(self, widget, event, icon):
        icon.selected = not icon.selected
        icon.grabbed = False

    def on_icon_gdk_motion_notify(self, widget, event, icon):
        if icon.grabbed:
            iw, ih = icon.image.get_width(), icon.image.get_height()
            x, y = event.x, event.y
            dispatcher.send(signal=icon, sender='gui', property='location',
                    old=icon.location, value=(x - iw, y - ih))

    def on_quit_activate(self, widget):
        self.quit()

    def on_Vellum_destroy(self, widget):
        self.quit()

    def quit(self):
        log.msg("Goodbye.")
        self.deferred.callback(None)

    def on_canvas_button_press_event(self, widget, ev):
        pass
    def on_canvas_button_release_event(self, widget, ev):
        pass
    def on_canvas_motion_notify_event(self, widget, ev):
        pass

