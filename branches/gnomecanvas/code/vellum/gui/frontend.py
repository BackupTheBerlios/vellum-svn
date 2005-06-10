import sys, os
# hack taken from <http://www.livejournal.com/users/glyf/7878.html>
import _winreg
def getGtkPath():
    subkey = 'Software/GTK/2.0/'.replace('/','\\')
    path = None
    for hkey in _winreg.HKEY_LOCAL_MACHINE, _winreg.HKEY_CURRENT_USER:
        reg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, subkey)
        for vname in ("Path", "DllPath"):
            try:
                try:
                    path, val = _winreg.QueryValueEx(reg, vname)
                except WindowsError:
                    pass
                else:
                    return path
            finally:
                _winreg.CloseKey(reg)

path = getGtkPath()
if path is None:
    raise ImportError("Couldn't find GTK DLLs.")
os.environ['PATH'] += ';'+path.encode('utf8')


# win32all
try:
    from win32ui import CreateFileDialog
    import win32con
except:
    def CreateFileDialog(*args, **kwargs):
        """TODO - use gtk one"""

# end goddamn ugly gtk hack
# end goddamn ugly gtk hack
# end goddamn ugly gtk hack

import gtk
from gtk import glade, gdk
import gnomecanvas

from twisted.python import log
from twisted.internet import task, reactor

from vellum.server import PBPORT
from vellum.gui.fs import fs


class Icon:
    """
    - image: the image used for the icon
    - xy: a 2-tuple specify the top-left corner of the icon
    """
    def __init__(self):
        self.image = None
        self.xy = (None, None)

class Model:
    """
    - background: the image used as the background (usually, a map)
    - icons: a list of icon objects
    """
    def __init__(self, background):
        self.background = background
        self.icons = []


class FrontEnd:
    def __getattr__(self, name):
        if name.startswith("gw_"):
            return self.glade.get_widget(name[3:])
        raise AttributeError, "%s instance has no attribute %s" % (
            self.__class__, name)

    def __init__(self, deferred, netclient, fps):
        self.fps = fps
        self.deferred = deferred
        self.netclient = netclient

        self.glade = glade.XML(fs.gladefile)
        self.glade.signal_autoconnect(self)

        # create a gnomecanvas
        self.canvas = gnomecanvas.Canvas() # FIXME: aa=True breaks text render
        self.canvas.show()
        self.gw_viewport1.add(self.canvas)

        # allocate the slate background
        self.bg = gdk.pixbuf_new_from_file(fs.background)
        self.canvas.set_size_request(self.bg.get_width(), self.bg.get_height())
        self.canvas.set_center_scroll_region(False)

        self.canvas.root().add("GnomeCanvasPixbuf", pixbuf=self.bg,
                               )

        # coordinate and scale for displaying the model
        self.scale = 1.0
        self.corner = (0,0)

        self.model = None
        # self.paintDefault()


    def on_Tester_destroy(self, widget):
        log.msg("Goodbye.")
        self.deferred.callback(None)

    def paintDefault(self):
        """Draw the default background"""
        tile_w = self.bg.get_width()
        tile_h = self.bg.get_height()
        # tile the texture
        root = self.canvas.root()
        if self.model is None:
            # root.add("GnomeCanvasPixbuf", x=0, y=0,
            #            pixbuf=self.bg)
            #root.add("GnomeCanvasPixbuf", x=-129, y=0,
            #            pixbuf=self.bg)
            root.add("GnomeCanvasRect", x1=0, x2=384, y1=0, y2=384,
                    fill_color="blue", outline_color="black")
            root.add("GnomeCanvasText", x=0, y=0, text="0,0")
            root.add("GnomeCanvasText", x=300, y=300, text="300,300")
            root.add("GnomeCanvasText", x=0, y=300, text="0,300")
            root.add("GnomeCanvasText", x=300, y=0, text="300,0")
            return # FIXME
            for x in range(num_x):
                for y in range(num_y):
                    root.add("GnomeCanvasPixbuf",
                             x=x*tile_w, 
                             y=y*tile_h,
                             pixbuf=self.bg)
        else:
            FIXME
            # self.main.blit(self.model.background, (0,0))
            # for icon in self.model.icons:
            #    self.main.blit(icon.image, icon.xy)

    def on_connect_button_clicked(self, widget):
        text = self.gw_server.get_child().get_text()
        d = self.netclient.startPb(text, PBPORT)
        d.addErrback(log.err)
        d.addCallback(self._cb_gotFileInfos)
        d.addCallback(lambda _: self.displayModel())

    def _getMapInfo(self):
        for fi in self.fileinfos:
            if fi['type'] == 'map':
                return fi

    def _getCharacterInfo(self):
        for fi in self.fileinfos:
            if fi['type'] == 'character':
                yield fi

    def displayModel(self):
        mapinfo = self._getMapInfo()
        log.msg('displaying map %s' % (mapinfo['name'],))
        self.model = Model(pygame.image.load(fs.downloads(mapinfo['name'])))
        self.main.blit(self.model.background, (0,0))
        for n, character in enumerate(self._getCharacterInfo()):
            icon_image = pygame.image.load(fs.downloads(character['name']))
            icon = Icon()
            self.model.icons.append(icon)
            icon.image = icon_image
            icon.xy = n*80, n*80
            self.main.blit(icon.image, icon.xy)
        # self.addCharacter
        # self.addItem
        # self.addText
        # self.addSound
        # self.clearObscurement()
        # self.obscure?

    def _cb_gotFileInfos(self, fileinfos):
        self.fileinfos = fileinfos
