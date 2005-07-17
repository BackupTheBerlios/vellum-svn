from wrapper import MyObject
from modifier import AggregateModifier, LevelAggregator

class CategoryDict( dict ):
    def __init__( self, aggregator, vals=None ):
        vals = vals or { }
        self.aggregator = aggregator
        self.crossdict = { }
        if not isinstance( vals, dict ):
            vals = dict( [ ( v.key, v ) for v in vals ] )
        for key, val in vals:
            self[ key ] = val

    def __delitem__( self, key ):
        try:
            mod = self.crossdict[ key ]
            del self[ mod.type ][ key ]
            del self.crossdict[ key ]
        except KeyError:
            for item in self[ key ]:
                del self[ item.key ]
            self[ key ] = self.aggregator( )

    def __getitem__( self, key ):
        try:
            return self.crossdict[ key ]
        except KeyError:
            return super( CategoryDict, self ).__getitem__( key )

    def __setitem__( self, key, val ):
        try:
            super( CategoryDict, self ).__getitem__( val.type ).extend( val )
        except TypeError:
            super( CategoryDict, self ).__getitem__( val.type ).append( val )
        except KeyError:
            if isinstance( val, AggregateModifier ):
                super( CategoryDict, self ).__setitem__( key, val )
                for item in val.values( ):
                    self.crossdict[ item.key ] = item
                return
            else:
                super( CategoryDict, self ).__setitem__( val.type, self.aggregator( [ val ] ) )
        self.crossdict[ key ] = val

    def keys( self, type=None ):
        if type:
            return self[ type ].keys( )
        else:
            return super( CategoryDict, self ).keys( )

    def iterkeys( self, type=None ):
        if type:
            return self[ type ].iterkeys( )
        else:
            return super( CategoryDict, self ).iterkeys( )

    def values( self, type=None ):
        if type:
            return self[ type ].values( )
        else:
            return super( CategoryDict, self ).values( )

    def itervalues( self, type=None ):
        if type:
            return self[ type ].itervalues( )
        else:
            return super( CategoryDict, self ).itervalues( )

    def items( self, type=None ):
        if type:
            return self[ type ].items( )
        else:
            return super( CategoryDict, self ).items( )

    def iteritems( self, type=None ):
        if type:
            return self[ type ].iteritems( )
        else:
            return super( CategoryDict, self ).iteritems( )

    def __str__( self ):
        return ("\n" + tabbies ).join( [ "%s: %s," % ( key, val or 0 ) for key, val in self.items( ) ] )

class ModifierDict( CategoryDict ):
    def __init__( self, aggregator=None, vals=None ):
        vals = vals or { }
        aggregator = aggregator or AggregateModifier
        super( ModifierDict, self ).__init__( aggregator, vals )

class LevelBox( CategoryDict ):
    def __init__( self, levels=None, eladjustment=0  ):
        self.eladjustment = eladjustment
        super( LevelBox, self ).__init__( LevelAggregator, levels )

    def addLevel( self, level ):
        self[ level.key ] = level

    def levels( self ):
        lvls = self.crossdict.values( )
        lvls.sort( )
        return lvls

    def __iter__( self ):
        return iter( self.levels( ) )

    def __int__( self ):
        return sum( [ int( lvls ) for lvls in self.values( ) ] )

    def __str__( self ):
        string = ""
        for key, val in self.items( ):
            string += "%s %s\n" % ( key, int( val ) )
        return string
