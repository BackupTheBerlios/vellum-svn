from resolve import Condition, IResolveable, Resolveable, Resolver
from zope.interface import interface, implements
from twisted.python import components
import types

#class MinAggregateModifier( AggregateModifier ):
#    def __init__( self, mods=None, target=None, type=None ):
#        super( MinAggregateModifier, self ).__init__( mods, min, target, type )

#class MaxAggregateModifier( AggregateModifier ):
#    def __init__( self, mods=None, target=None, type=None ):
#        super( MaxAggregateModifier, self ).__init__( mods, max, target, type )

#class LevelAggregator( AggregateModifier ):
#    def append( self, level ):
#        self.mods[ level.key ] = level

