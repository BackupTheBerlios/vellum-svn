import sys

import gtk
import gnomecanvas
from gnomecanvas import MOVETO_OPEN as MO, MOVETO as M, LINETO as L


from math import sin, cos, pi, atan

def affineRotationForAngle(radians, x, y):
    """Pass in radians.  Returns a 6-tuple"""
    scalex = cos(radians)
    sheary = sin(-radians)
    shearx = sin(radians)
    scaley = scalex
    return (scalex, sheary, shearx, scaley, x, y)

def affineScaleForFactor(factor, x, y):
    return (factor, 0, 0, factor, x, y)




class Square:
    def __init__(self, canvas, center=(0,0), edge_length=100, color="gray"):
        self.center = center
        self.edge_length = edge_length
        self.color = color

        self.canvas = canvas

        self.draw(center)

        self.grabbed = False
        self.selected = False

    def _getCorners(self, coords):
        return (coords[0]-self.edge_length/2.,
                coords[1]-self.edge_length/2.,
                coords[0]+self.edge_length/2.,
                coords[1]+self.edge_length/2.,
                )

    def draw(self, coords):
        x1,y1,x2,y2=self._getCorners(coords)
        self.widget = self.canvas.root().add("GnomeCanvasRect",
                                             x1=x1,y1=y1,x2=x2,y2=y2,
                                             fill_color=self.color,
                                             )

    def move(self, x, y):
        # adjust so the center is drawn at the coordinates
        x, y, _, _ = self._getCorners((x,y))
        self.widget.move(x,y)

    def connect(self, *args, **kwargs):
        self.widget.connect(*args, **kwargs)

class Arrow:
    def __init__(self, canvas, origin=(0,0), target=(0,0), color="gray"):
        self.canvas = canvas
        self.color = color
        self.createShaft(origin, target)
        self.attachHead(origin, target)

        self.origin = origin
        self.target = target

    def createShaft(self, origin, target):
        pd = gnomecanvas.path_def_new([(MO, origin[0], origin[1]), 
                                       (L, target[0], target[1])])
        
        self.shaft = self.canvas.root().add("GnomeCanvasBpath",
                                       width_pixels=5,
                                       cap_style=gtk.gdk.CAP_ROUND,
                                       outline_color=self.color)
        self.shaft.set_bpath(pd)

    def attachHead(self, origin, target):
        tx, ty = map(float, target)
        sx, sy = tx-20, ty
        ex, ey = tx, ty+20

        ox, oy = map(float, origin)

        _p = gnomecanvas.path_def_new([(MO, sx, sy),
                                       (L, tx, ty),
                                       (L, ex, ey),
                                       ])
        self.head = self.canvas.root().add("GnomeCanvasBpath",
                                      width_pixels=5,
                                      cap_style=gtk.gdk.CAP_ROUND,
                                      outline_color=self.color,
                                      )
        self.head.set_bpath(_p)
        if oy != ty:
            # negate the y axis due to stupid display coordinates
            leg_ratio = (tx-ox)/(oy-ty)
            tip_angle = atan(leg_ratio)
        else:
            # avoid zerodivisionerror...
            if tx > ox:
                tip_angle = pi/2
            else:
                tip_angle = 3*pi/2
        correction_angle = pi/4 - tip_angle
        # flip 180 degrees if arrow is pointing down
        if ty > oy: correction_angle = correction_angle + pi
        affines = affineRotationForAngle(correction_angle, tx, ty)

        self.head.affine_relative(affines)
        self.head.move(-tx, -ty)

    def move(self, origin=None, target=None):
        self.shaft.destroy()
        self.head.destroy()
        if origin is not None:
            self.origin = origin
        else:
            origin = self.origin
        if target is not None:
            self.target = target
        else:
            target = self.target
        self.createShaft(origin, target)
        self.attachHead(origin, target)



class Canvassy(gnomecanvas.Canvas):
    def __init__(self, *args, **kwargs):
        gnomecanvas.Canvas.__init__(self)
        self.set_center_scroll_region(False)
        # background white
        self.rect = self.root().add("GnomeCanvasRect", x1=0, y1=0, 
                                    x2=500, y2=500,
                                    fill_color="#ffffff")

        self.root().add("GnomeCanvasText", x=125,y=25, text="Move the red square")

        # shapes and stuffs
        origin = (100, 50)
        target = (150, 150)
        blue = Square(self, center=origin, color="#0000ff", edge_length=30)
        red = Square(self, center=target, color="#ff0000", edge_length=30)

        self.arrow = Arrow(self, origin=origin, target=target, color="#000000")

        red.connect('event', self.on_square_event, red)
        blue.connect('event', self.on_square_event, blue)

    def on_square_event(self, widget, event, square):
        type = event.type.value_name.lower()
        handler = getattr(self, 'on_square_%s' % (type,), None)
        if handler is not None:
            return handler(widget, event, square)

    def on_square_gdk_button_press(self, widget, event, square):
        # left click
        if event.button == 1:
            square.grabbed = True

    def on_square_gdk_button_release(self, widget, event, square):
        if event.button == 1:
            square.selected = not square.selected
            square.grabbed = False

    def on_square_gdk_motion_notify(self, widget, event, square):
        if square.grabbed:
            startx, starty, _, _ = widget.get_bounds()
            square.move(event.x - startx, event.y - starty)
            self.arrow.move(target=(event.x, event.y))
            


def destroy(event):
    gtk.main_quit()

def run(argv=None):
    if argv is None:
        argv = sys.argv

    w = gtk.Window()
    w.connect('destroy', destroy)
    c = Canvassy()
    w.add(c)
    w.show_all()

    gtk.main()
    return 0


if __name__ == '__main__':
    sys.exit(run())

