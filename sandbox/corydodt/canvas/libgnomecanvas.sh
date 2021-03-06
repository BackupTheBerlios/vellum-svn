#!/bin/bash
set -e
set -x

echo This should be considered a Proof of Concept.  Use muntyan\'s \
libgnomecanvas binaries for real work.

echo Can\'t have Cygwin\'s libintl in the static library search PATH
[ ! -r /usr/lib/libintl.a -a ! -r /usr/lib/libintl.la -a ! -r /usr/lib/libintl.dll.a ] || exit 1

CFLAGS="-mno-cygwin -mms-bitfields -IC:/PROGRA~1/COMMON~1/GTK/include"
ENV=env CPPFLAGS="$CPPFLAGS" CFLAGS="$CFLAGS" 

# not using -mingw32 as the host causes the .dll to have the name
# "cyggnomecanvas".  suck.
$ENV CFLAGS="$CFLAGS" ./configure --prefix="`pwd`/dist"

# using -mingw32 as the host causes .dll to not compile at all. suck. FIXME.
#$ENV CFLAGS="$CFLAGS" ./configure --prefix="`pwd`/dist" \
#                                               --build=i686-pc-mingw32 \
#                                               --host=i686-pc-mingw32 \
#                                               --target=i686-pc-mingw32

$ENV CFLAGS="$CFLAGS" make
$ENV CFLAGS="$CFLAGS" make install
