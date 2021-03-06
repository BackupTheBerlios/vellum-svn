"""HTTP and PB client."""

import md5

from twisted.internet import reactor, defer
from twisted.spread import pb
from twisted.python import log
from twisted.web.client import downloadPage

from vellum.gui.fs import fs
from vellum.server import HTTPPORT

def _cb_connected(pbobject):
    log.msg('connected %s' % (repr(pbobject,)))
    return pbobject


class NetClient:
    def __init__(self):
        self.pbfactory = pb.PBClientFactory()

    def startPb(self, server, port):
        self.server = server
        reactor.connectTCP(server, port, self.pbfactory)
        d = self.pbfactory.getRootObject()
        d.addErrback(lambda reason: 'error: '+str(reason.value))
        d.addCallback(_cb_connected)
        d.addCallback(lambda pbobject: 
                        pbobject.callRemote('listAvailableFiles')
                      )
        d.addCallback(self.getMapInfo)
        return d

    def getMapInfo(self, map):
        self.map = map
        fileiter = iter(map['files'])
        d = defer.maybeDeferred(self._getNextFile, fileiter)
        # TODO - this might be called after the first _getNextFile instead of
        # the intended behavior, after the last one.  Please check.
        d.addCallback(lambda _: map['files'])
        return d

    def _getNextFile(self, fileinfos):
        try:
            fi = fileinfos.next()
            try:
                # do we already have the file? let's find out.
                self.checkFile(fi)
                return defer.maybeDeferred(self._getNextFile, fileinfos)
            except ValueError:
                log.msg('Getting file at %s' % (fi['uri'],))
                uri = 'http://%s:%s/%s' % (self.server,
                                           HTTPPORT,
                                           fi['uri'],
                                           )
                return downloadPage(uri, fs.downloads(fi['name'])
                        ).addErrback(log.err
                        ).addCallback(lambda _: self.checkFile(fi)
                        ).addCallback(lambda _: self._getNextFile(fileinfos)
                        )
        except StopIteration:
            return

    def checkFile(self, fileinfo):
        try:
            f = file(fs.downloads(fileinfo['name']), 'rb')
            digest = md5.md5(f.read()).hexdigest()
            print 'Got file; checksum:', digest
            if digest == fileinfo['md5']:
                print 'md5 ok for %s' % (fileinfo['name'],)
                return
        except EnvironmentError:
            pass
        raise ValueError("File was not received correctly: %s" % (
            str(fileinfo),))
        
