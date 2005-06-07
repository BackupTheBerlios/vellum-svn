#!/bin/bash
set -e
set -x

# (./configure only needed to generate the Makefile, which we don't use.)
# CFLAGS="-mno-cygwin -mms-bitfields -Ic:/python23/include" 
# PKG_CONFIG_PATH="C:/cygwin/target/lib/pkgconfig;c:/python23/lib/pkgconfig"
# PATH="/c/python23/bin":"$PATH"
# env PKG_CONFIG_PATH="$PKG_CONFIG_PATH" \
#     CFLAGS="$CFLAGS" \
#     CPPFLAGS="$CFLAGS" \
#     PATH="$PATH" \
#     ./configure
# (make only needed to get the codegen command below)
# make canvas.c


# generate canvas.c
/c/python23/bin/pygtk-codegen-2.0 \
    --register C:\\PYTHON23/share/pygtk/2.0/defs/pango-types.defs \
    --register C:\\PYTHON23/share/pygtk/2.0/defs/gdk-types.defs \
    --register C:\\PYTHON23/share/pygtk/2.0/defs/gtk-types.defs \
    --override canvas.override \
    --prefix pycanvas canvas.defs > canvas.c


# environment
CFLAGS="-mno-cygwin -mms-bitfields -O -Wall -DNDEBUG=1"
INCLUDES="
    -I.  \
    -Ic:/python23/include \
    -IC:/python23/include/pygtk-2.0 \
    -I/target/lib/glib-2.0/include \
    -I/target/lib/gtk-2.0/include \
    -I/target/include/glib-2.0 \
    -I/target/include/gtk-2.0 \
    -I/target/include/atk-1.0 \
    -I/target/include/libart-2.0 \
    -I/target/include/libglade-2.0 \
    -I/target/include/libgnomecanvas-2.0 \
    -I/target/include/pango-1.0 \
    -I/target/include"

# compile
gcc $CFLAGS -mdll -DALL_STATIC=1 $INCLUDES -c canvas.c -o canvas.o

gcc $CFLAGS -mdll -DALL_STATIC=1 $INCLUDES -c canvasmodule.c -o canvasmodule.o

# link
gcc $CFLAGS -shared -s canvas.o canvasmodule.o \
    -LC:/python23/libs \
    -L/target/lib/glib-2.0 \
    -L/target/lib/gtk-2.0 \
    -L/target/lib/libart-2.0 \
    -L/target/lib/libglade-2.0 \
    -L/target/lib/libgnomecanvas-2.0 \
    -L/target/lib \
    -lgnomecanvas-2 \
    -lpython23 \
    -lglib-2.0 \
    -lgtk-win32-2.0 \
    -lgdk-win32-2.0 \
    -lgobject-2.0 \
    -o gnomecanvas.pyd

