import warnings; warnings.filterwarnings('ignore')

from twisted.application import service, internet
from twisted.spread import pb

from net import createPortal

application = service.Application('ReVellum')


pbsvc = internet.TCPServer(9559, pb.PBServerFactory(createPortal()))

pbsvc.setServiceParent(application)

