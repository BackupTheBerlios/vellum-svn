import gtk
from gtk import gdk
try:
    from gnome import canvas as gnomecanvas
except ImportError:
    import gnomecanvas

class Foo:
    # Create a new backing pixmap of the appropriate size
    def scrape(self, canvas):
        x, y, ww, hh = canvas.get_allocation()
        self.scraped = gdk.Pixmap(canvas.window, ww, hh)
        self.scraped.draw_drawable(self.scraped.new_gc(),
                                   canvas.window, 
                                   0, 0, 0, 0, ww, hh)


    def copyDuplicateToCanvas(self, canvas):
        x, y, ww, hh = canvas.get_allocation()
        pixbuf = gdk.Pixbuf(colorspace=gdk.COLORSPACE_RGB, 
                            has_alpha=True,
                            bits_per_sample=8, 
                            width=ww, 
                            height=hh)
        pixbuf.get_from_drawable(self.duplicate,
                canvas.window.get_colormap(),
                0, 0, 0, 0, ww, hh)
        pixbuf = pixbuf.add_alpha(True, *'\0\0\0')
        canvas.root().add("GnomeCanvasPixbuf", pixbuf=pixbuf, x=0, y=0)
        # TODO
        # - remove the current obscurement gnomecanvaspixbuf and replace it
        
    def switch(self, widget, event, page, canvas):
        if page == 1:
            # get a scrape from the canvas
            self.scrape(canvas)
        else:
            # if the duplicate has been edited, convert it
            if self.duplicate is not None:
                self.copyDuplicateToCanvas(canvas)



    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        notebook = gtk.Notebook()
        window.add(notebook)
        notebook.show()

        window.connect("destroy", lambda w: gtk.main_quit())

        # Create the drawing area
        canvas = gnomecanvas.Canvas()
        canvas.set_center_scroll_region(False)
        canvas.set_size_request(200, 200)

        drawing_area = gtk.DrawingArea()
        notebook.append_page(canvas, gtk.Label("Canvas"))
        notebook.append_page(drawing_area, gtk.Label("Drawing Area"))


        notebook.connect("switch-page", self.switch, canvas)
        drawing_area.connect("expose-event", self.expose_drawing, )
        drawing_area.connect("button-press-event", self.button_press, )
        drawing_area.connect("button-release-event", self.button_release, )
        drawing_area.connect("motion-notify-event", self.motion_notify, )

        canvas.set_events(gdk.ALL_EVENTS_MASK)
        notebook.set_events(gdk.ALL_EVENTS_MASK)
        drawing_area.set_events(gdk.ALL_EVENTS_MASK)


        canvas.root().add("GnomeCanvasPixbuf",
            pixbuf=gdk.pixbuf_new_from_file("slatebg.png"),
            x=0, y=0)

        self.scraped = None
        self.last_brush = None
        self.duplicate = None

        window.show_all()

        gtk.main()

    def paint(self, widget, x, y):
        x = int(x)
        y = int(y)
        rect = (x-5, y-5, 10, 10)
        white = widget.get_style().white_gc
        if self.last_brush is not None:
            gc2 = widget.window.new_gc()
            gc2.copy(white)
            gc2.set_line_attributes(10, gtk.gdk.LINE_SOLID,
                    gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_BEVEL)
            self.scraped.draw_lines(gc2, [(x,y), self.last_brush])

            # paint the same thing to a duplicate so we can get the
            # drawn pixels without the background
            if self.duplicate is None:
                # delay creating the duplicate until here so it's easy to
                # check if it's been modified
                x, y, ww, hh = widget.get_allocation()
                self.duplicate = gdk.Pixmap(widget.window, ww, hh)
            self.duplicate.draw_lines(gc2, [(x,y), self.last_brush])

        widget.queue_draw()
        self.last_brush = x, y


    def button_press(self, w, ev):
        self.paint(w, ev.x, ev.y)

    def button_release(self, w, ev):
        self.last_brush = None

    def motion_notify(self, w, ev):
        state = ev.get_state()
        if self.scraped is not None and state == gtk.gdk.BUTTON1_MASK:
            self.paint(w, ev.x, ev.y)

    def expose_drawing(self, w, ev):
        x, y, ww, hh = map(int, ev.area)
        if self.scraped is not None:
            fg_gc = w.get_style().fg_gc[gtk.STATE_NORMAL]
            w.window.draw_drawable(fg_gc, self.scraped, x, y, *ev.area)

if __name__ == "__main__":
    Foo()
