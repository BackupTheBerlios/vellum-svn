from wrapper import MyObject, tabbies
from dict import ModifierDict
from modifier import AggregateModifier, ModifierFactory, MultipliedModifierFactory

class Attribute( MyObject ):
    lastkey = 0

    def __init__( self, name, number, aggregator=None ):
        aggregator = aggregator or AggregateModifier
        self.name = name
        self.number = number
        self.modifiers = ModifierDict( aggregator )
        self.key = "%s %s" % ( self.__class__.__name__, self.lastkey )
        Attribute.lastkey += 1
        self.situation = False

    def __add__( self, other ):
        return int( self ) + other
    __radd__ = __add__

    def __cmp__( self, other ):
        import math
        diff = self - other
        return diff and diff / math.fabs( diff ) or diff

    def __int__( self ):
        vals = [ ]
        for m in self.modifiers.values( ):
            try:
                vals.append( int( m ) )
            except:
                pass
        return self.number + sum( vals )

    def __neg__( self ):
        return -int( self )

    def __str__( self ):
        fixings = ""
        global tabbies
        tabbies += "\t"
        for mod in [ self.number ] + self.modifiers.values( ):
            s = str( mod )
            if s != '\b':
                fixings += "\n%s%s" % ( tabbies, s )
        tabbies = tabbies[ :-1 ]
        return "%s: " % self.name + "%s" % int( self ) + fixings

    def __sub__( self, other ):
        return self  + ( -other )
    __rsub__ = __sub__

    def resolveForSituation( self, situation ):
        sit = self.situation
        self.situation = situation
        ammount = int( self )
        self.situation = sit
        return ammount

    #Properties
    def getNumber( self ):
        return self._number( )

    def setNumber( self, number ):
        self._number = callable( number ) and number or ( lambda: number )
    number = property( fget=getNumber, fset=setNumber, doc="This Attribute's base value" )

class Stat( Attribute ):
    def __init__( self, name, number, modprovided=None, aggregator=None ):
        super( Stat, self ).__init__( name, number, aggregator )
        self.mod = modprovided or self.__int__

    def applyMods( self ):
        for mod in self.modprovided:
            mod.addToTargets( )

    def revokeMods( self ):
        for mod in self.modprovided:
            mod.removeFromTargets( )

    #Properties
    def getMod( self ):
        return self.modprovided

    def setMod( self, value ):
        try:
            self.modprovided.number = value
        except:
            self.modprovided = ModifierFactory( self, value )
    mod = property( fget=getMod, fset=setMod, doc="The modifier this Stat provides" )

class Continuum( Stat ):
    def __init__( self, magnitude, name=None, ranks=None, names=None ):
        self.ranks = ranks or Continuum.sizeRanks
        self.names = names or Continuum.sizeNames
        name = name or 'Continuum'
        if isinstance( magnitude, Continuum ):
            magnitude = magnitude.magnitude
        elif isinstance( magnitude, str ):
            magnitude = dict( [ ( val, key ) for key, val in self.sizeRanks.items( ) ] )[ magnitude ]
        super( Continuum, self ).__init__( name, magnitude, self.__int__ )

    def __add__( self, other ):
        return self.__init__( self.number + other )
    __radd__ = __add__

    def __sub__( self, other ):
        return self.__init__( self.number - other )
    __rsub__ = __sub__

    def __int__( self ):
        try:
            magnitude = super( Continuum, self ).__int__( )
            absval = abs( magnitude )
            vector = magnitude/ absval
            return ( 2 ** ( absval - 1 ) ) * vector
        except:
            return 0

    def __str__( self ):
        try:
            magnitude = super( Continuum, self ).__int__( )
            category = "%s (%s)" % ( self.ranks[ magnitude ], self.names[ magnitude ] )
        except:
            category = "No category for this size"
        return category

    #Properties
    def getLetter( self ):
        return self.ranks[ super( Continuum, self ).__int__( ) ]
    letter = property( fget=getLetter, doc="The letter of this size" )

    sizeRanks = dict( zip( range( -4, 5 ), [ 'F', 'D', 'T', 'S', 'M', 'L', 'H', 'C', 'G', ] ) )
    sizeNames = dict( zip( range( -4, 5 ), [ "Fine", "Diminuative", "Tiny", "Small", "Medium", "Large", "Huge", "Collosal", "Gargantuan" ] ) )
