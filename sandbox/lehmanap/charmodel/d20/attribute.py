from charmodel.generic.attribute import Attribute, Continuum, Stat
from charmodel.generic.modifier import AggregateModifier, CappedAggregateModifier, MaxAggregateModifier

class D20Attribute( Attribute ):
    def __init__( self, name, number ):
        super( D20Attribute, self ).__init__( name, number, aggregator=MaxAggregateModifier )
        self.modifiers[ 'INNATE' ] = CappedAggregateModifier( 5, target=self )
        self.modifiers[ 'RANKS' ] = AggregateModifier( target=self )

class D20CritRange( D20Attribute ):
    def __init__( self, rng ):
        super( D20Attribute, self ).__init__( 'Critical Hit Threat Range', len( range( rng[ 0 ], rng[ 1 ] + 1 ) ) )

    def __iter__( self ):
        return iter( range( 20, 0, -1 )[ :int( self ) ] )

    def __contains__( self, val ):
        return val in range( 20, 0, -1 )[ :int( self ) ]

    def __str__( self ):
        first = range( 1, 21 )[ -int( self ) ]
        return "%s%s" % ( first, first != 20 and "-20" or "" )

class D20Size( Continuum ):
    def __init__( self, magnitude ):
        super( D20Size, self ).__init__( magnitude, 'Size' )

class D20DamageRange( Continuum ):
    def __init__( self, magnitude, dieroll ):
        row = dict( [ ( dierow[ 4 ], rownum ) for rownum, dierow in enumerate( D20DamageRange.rankTable ) ] )[ dieroll ]
        ranks = dict( zip( range( -4, 5 ), self.rankTable[ row ] ) )
        super( D20DamageRange, self ).__init__( magnitude, 'Size', 
                                            ranks=ranks )

    def roll( self ):
        from vellum.server.dice import parse
        return parse( self.ranks[ super( D20DamageRange, self ).__int__( ) ] )[ 0 ].sum( )

    rankTable=[
[ '0',      '0',      '0',      '1',      '1d2',    '1d3',    '1d4',    '1d6',    '1d8' ],
[ '0',      '0',      '1',      '1d2',    '1d3',    '1d4',    '1d6',    '1d8',    '2d6' ],
[ '0',      '1',      '1d2',    '1d3',    '1d4',    '1d6',    '1d8',    '2d6',    '3d6' ],
[ '1',      '1d2',    '1d3',    '1d4',    '1d6',    '1d8',    '2d6',    '3d6',    '4d6' ],
[ '1d2',    '1d3',    '1d4',    '1d6',    '2d4',    '2d6',    '3d6',    '4d6',    '6d6' ],
[ '1d2',    '1d3',    '1d4',    '1d6',    '1d8',    '2d6',    '3d6',    '4d6',    '6d6' ],
[ '1d3',    '1d4',    '1d6',    '1d8',    '1d10',   '2d8',    '3d8',    '4d8',    '6d8' ],
[ '1d4',    '1d6',    '1d8',    '1d10',   '1d12',   '3d6',    '4d6',    '6d6',    '8d6' ],
[ '1d4',    '1d6',    '1d8',    '1d10',   '2d6',    '3d6',    '4d6',    '6d6',    '8d6' ],
                ]

class D20Stat( Stat ):
    def __init__( self, name, number, modsprovided=None, aggregator=None ):
        super( D20Stat, self ).__init__( name, number, modsprovided, aggregator )
        self.modifiers[ 'INNATE' ] = CappedAggregateModifier( 5, target=self )
        self.modifiers[ 'RANKS' ] = AggregateModifier( target=self )

class D20HP( D20Stat ):
    def __init__( self, name, number ):
        super( D20HP, self ).__init__( name, number )
        self.mod = lambda: max( 1, int( self ) )

class D20Damage( D20Stat ):
    def __init__( self, types, size=0, roll="1d8", range=None ):
        self.range = range or D20DamageRange( size, roll )
        self.types = types
        super( D20Damage, self ).__init__( 'Damage', 0, self.__int__ )
        self.mod.static = True

    def __str__( self ):
        return "%s + %s" % ( self.range, self.modifiers )

    #Properties
    def getNumber( self ):
        return int( self.range.roll( ) ) + super( D20Damage, self ).number
    number = property( fget=getNumber, fset=D20Attribute.number.fset, fdel=D20Attribute.number.fdel )

class D20Critical( D20Damage ):
    def __init__( self, types, multiplierfunc, size=0, roll="1d8", range=None ):
        super( D20Critical, self ).__init__( types, size, roll, range )
        self.multiplierfunc = multiplierfunc

    def __str__( self ):
        return "( %s ) x %s" % ( super( D20Critical, self ).__str__( ), self.multiplierfunc( ) )

    #Properties
    def getNumber( self ):
        sum = 0
        for i in range( self.multiplierfunc( ) ):
            sum += int( self.range.roll( ) ) + super( D20Damage, self ).number
        return sum
    number = property( fget=getNumber, fset=D20Attribute.number.fset, fdel=D20Attribute.number.fdel )

    def __int__( self ):
        sum = 0
        for i in range( self.multiplierfunc( ) ):
            sum += int( self.range.roll( ) ) + super( D20Damage, self ).__int__( )
        return sum

class D20AbilityScore( D20Stat ):
    def __init__( self, name, number ):
        import math
        super( D20AbilityScore, self ).__init__( name, number, aggregator=MaxAggregateModifier )
        self.mod = lambda: int( math.floor( ( int( self ) - 10 ) / 2 ) )

class D20Skill( D20Stat ):
    def __init__( self, name, number ):
        super( D20Skill, self ).__init__( name, number, aggregator=MaxAggregateModifier )

