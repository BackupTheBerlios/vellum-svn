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
from model import Note, Icon, New, Drop



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

        self.rect = canvas.root().add(
                "GnomeCanvasRect", x1=0, y1=0, x2=500, y2=500,
                fill_color="#ffffff")
        self.rect.connect('event', c.on_background_event, self.rect)

        w.connect('destroy', c.on_Vellum_destroy)

        self.canvas = canvas

class BigController:
    def __init__(self, deferred):
        self.deferred = deferred

    def receiveNewModel(self, sender, model): 
        receiver = getattr(self, 'new_%s' % (model.__class__.__name__))
        receiver(model)

    def receiveDropModel(self, sender, model): 
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
    changed_Note_location = changed_Icon_location

    def drop_Icon(self, icon):
        if getattr(icon, 'widget', None) is not None:
            icon.widget.destroy()
            icon.widget = None
    drop_Note = drop_Icon

    def changed_Note_text(self, note, sender, old, new):
        note.set_property('text', new)



    def new_Icon(self, icon):
        # clean up icon if necessary
        if getattr(icon, 'widget', None) is not None:
            icon.widget.destroy()
            icon.widget = None

        # make an image
        image = icon.image = gdk.pixbuf_new_from_file(fs.crom)

        # place it on the canvas
        root = self.view.canvas.root()
        corner = icon.location
        if corner is None: corner = (0,0)
        x, y = corner
        if icon.widget is None:
            igroup = root.add("GnomeCanvasGroup", x=x, y=y)
            igroup.add("GnomeCanvasPixbuf",
                       pixbuf=image,
                       x=0, y=0)


            igroup.connect('event', self.on_Icon_event, icon)
            icon.widget = igroup

    def new_Note(self, note):
        if getattr(note, 'widget', None) is not None:
            note.widget.destroy()
            note.widget = None

        # place text on the canvas
        root = self.view.canvas.root()
        corner = note.location
        if corner is None: corner = (0,0)
        x, y = corner
        if note.widget is None:
            ngroup = root.add("GnomeCanvasGroup", x=x, y=y)
            ngroup.add("GnomeCanvasText",
                    text=note.text,
                    x=0, y=0)

            ngroup.connect('event', self.on_Note_event, note) # FIXME: *note*_event
            note.widget = ngroup



    def on_Note_event(self, widget, event, note):
        type = event.type.value_name.lower()
        handler = getattr(self, 'on_Note_%s' % (type,), None)
        if handler is not None:
            return handler(widget, event, note)
    def on_Icon_event(self, widget, event, icon):
        type = event.type.value_name.lower()
        handler = getattr(self, 'on_Icon_%s' % (type,), None)
        if handler is not None:
            return handler(widget, event, icon)

    def on_background_event(self, widget, event, background):
        type = event.type.value_name.lower()
        handler = getattr(self, 'on_background_%s' % (type,), None)
        if handler is not None:
            return handler(widget, event, background)

    def on_Icon_gdk_button_press(self, widget, event, icon):
        # left click
        if event.button == 1:
            icon.grabbed = True
    on_Note_gdk_button_press = on_Icon_gdk_button_press

    def on_Icon_gdk_button_release(self, widget, event, icon):
        if event.button == 1:
            icon.selected = not icon.selected
            icon.grabbed = False
        elif event.button == 3:
            dispatcher.send(signal=Drop,
                            sender='gui',
                            model=icon)
    on_Note_gdk_button_release = on_Icon_gdk_button_release


    def on_Icon_gdk_motion_notify(self, widget, event, icon):
        if icon.grabbed:
            ix1, iy1, ix2, iy2 = icon.widget.get_bounds()
            iw, ih = ix2 - ix1, iy2 - iy1
            x, y = event.x, event.y
            dispatcher.send(signal=icon, 
                            sender='gui', 
                            property='location',
                            old=icon.location, 
                            value=(x - iw, y - ih))
    on_Note_gdk_motion_notify = on_Icon_gdk_motion_notify

    def on_quit_activate(self, widget):
        self.quit()

    def on_Vellum_destroy(self, widget):
        self.quit()

    def quit(self):
        log.msg("Goodbye.")
        self.deferred.callback(None)

    def on_background_gdk_button_release(self, widget, ev, background):
        """on right click make a new icon"""
        if ev.button == 3:
            # create a new Icon, and move it to the position of click
            icon = Icon()
            dispatcher.send(signal=New, 
                            sender='gui', 
                            model=icon)
            dispatcher.send(signal=icon, 
                            sender='gui', 
                            property='location', 
                            old=icon.location,
                            value=(ev.x, ev.y)
                            )

