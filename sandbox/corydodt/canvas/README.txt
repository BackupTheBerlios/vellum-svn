These are the components needed to build libgnomecanvas and its Python
bindings.

* libgnomecanvas-bin-muntyan-2.10.0.tar.bz2
    Binaries for libgnomecanvas.   Extract to your GTK directory for the 
    libgnomecanvas runtime.
* gnomecanvas-bindings-muntyan-2.11.2.tar.gz
    A package made by muntyan which provides gnomecanvas bindings in isolation
    (i.e. without the rest of gnome-python, which is neither necessary nor
    compilable).  Untar.
* gnomecanvas-bindings.sh
    A shell script for compiling the gnomecanvas bindings provided by muntyan.
    Run it in the untarred directory.

Also:
* libgnomecanvas.sh
    A shell script for compiling the libgnomecanvas runtime from source.
    Currently it is flawed, as it gives the DLL the name "cyggnomecanvas"
    instead of "libgnomecanvas".  In theory this name problem should go away
    by passing "--host=i686-pc-mingw32 --build=... --target=..."; but with
    these settings the DLL doesn't compile at all.

INSTRUCTIONS:
1. Extract the libgnomecanvas binaries to your GTK dir
2. Extract the source for the bindings to a directory with no spaces
3. cd gnomecanvas-2.11.2
4. Run gnomecanvas-bindings.sh

You will end up with a .pyd in the same directory, which you can copy to
site-packages.

