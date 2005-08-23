import warnings; warnings.filterwarnings('ignore')

from twisted.application import service, internet
from twisted.spread import pb

from peebee import gameportal

application = service.Application('ReVellum')


pbsvc = internet.TCPServer(9559, pb.PBServerFactory(gameportal))

pbsvc.setServiceParent(application)

