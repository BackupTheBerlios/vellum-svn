import sys, os

class Filesystem:
    def __init__(self, path, mkdir=0):
        if mkdir:
            try:
                os.makedirs(path)
            except EnvironmentError:
                pass
        self.path = os.path.abspath(path)

    def __call__(self, *paths):
        return os.path.join(self.path, *paths)
 
    def new(self, *paths, **kwargs):
        mkdir = kwargs.get('mkdir', 0)
        return Filesystem(os.path.join(self.path, *paths), mkdir=mkdir)

# for py2exe, make sure __file__ is real
if not os.path.isfile(__file__):
    __file__ = sys.executable


fs = Filesystem(os.getcwd())


fs.gladefile = fs("vellum.glade")
fs.saved = fs("mappy.yml")
fs.passwords = fs("vpasswd")

fs.crom = fs("crom.png")

