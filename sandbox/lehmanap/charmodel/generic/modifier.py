from wrapper import MyObject, Condition, Conditionable, tabbies

class Modifier( MyObject ):
    def __init__( self, type, parent, target, conditions, value=None ):
        self.type = type
        self.parent = parent
        self.target = target
        self.__int__.add( conditions or Condition( conditions ) )
        if value is not None:
            self.value = value

    def __add__( self, other ):
        try:
            return int( self ) + other
        except:
            return other
    __radd__ = __add__

    def __int__( self ):
        return getattr( self, 'value', int( self.parent ) )
    __int__ = Conditionable( __int__ )

    def __str__( self ):
        try:
            num = int( self )
            return str( self.parent )
        except:
            return "\b"

    #Properties
    def getKey( self ):
        return self.parent.key
    key = property( fget=getKey, doc="The unique key for this Modifier's ModifierFactory" )

    def getNumber( self ):
        return getattr( self, 'value', self.parent.number )
    number = property( fget=getNumber, doc="This Attributes base value" )

class MultipliedModifier( Modifier ):
    def __init__( self, mod, multiplier ):
        self.mod = mod
        self.multiplier = multiplier
        self.type = mod.type

    def __int__( self ):
        sum = int( self.mod )
        for x in range( self.multiplier - 1 ):
            #Done this way so that I can use this for Critical hits.
            sum += int( self.mod )
        return sum
    __int__ = Conditionable( __int__ )

    def __str__( self ):
        try:
            if self.multiplier != 1:
                return "%s = %s x %s" % ( int( self ), self.multiplier , str( self.mod ) )
            else:
                return str( self.mod )
        except:
            return "\b"

    def getNumber( self ):
        return self.multiplier * self.parent.number
    number = property( fget=getNumber, doc="This Attributes base value" )

    def getParent( self ):
        return self.mod.parent
    parent = property( fget=getParent, doc="This modifier's parent" )

    def getTarget( self ):
        return self.mod.target
    target = property( fget=getTarget, doc="This modifier's target" )

    def getConditions( self ):
        return self.mod.conditions
    conditions = property( fget=getConditions, doc="This modifier's conditions" )

class AggregateModifier( Modifier ):
    def __init__( self, mods=None, selector=sum, target=None, type=None ):
        mods = mods or [ ]
        self.mods = { }
        self.target = None
        self.type = None
        self.selector = selector
        for mod in mods:
            try:
                self.extend( mod )
            except TypeError:
                self.append( mod )

    def __delitem__( self, key ):
        del self.mods[ key ]

    def __getitem__( self, key ):
        return self.mods[ key ]

    def __setitem__( self, key, val ):
        self.mods[ key ] = val

    def __iter__( self ):
        return self.iterkeys( )

    def keys( self ):
        return self.mods.keys( )

    def values( self ):
        return self.mods.values( )

    def items( self ):
        return self.mods.items( )

    def iterkeys( self ):
        return self.mods.iterkeys( )

    def itervalues( self ):
        return self.mods.itervalues( )

    def iteritems( self ):
        return self.mods.iteritems( )

    def __int__( self ):
        return self.getNumber( )
    __int__ = Conditionable( __int__ )

    def __str__( self ):
        return ( '\n' + tabbies ).join( [ str( mod ) for mod in self.mods.itervalues( ) ] )

    def getNumber( self ):
        vals = [ ]
        for m in self.mods.values( ):
            try:
                vals.append( int( m ) )
            except:
                pass
        if vals:
            return self.selector( vals )
        elif self.mods.values( ):
            raise "I don't modify %s under these circumstances" % self.target.name
        else:
            return 0
    number = property( fget=getNumber, doc="This Attributes base value" )

    def append( self, mod ):
        if self.type is None or self.type == mod.type:
            self.type = mod.type
            if self.target is None or self.target == mod.target:
                self.target = mod.target
                self.mods[ mod.key ] = mod

    def extend( self, mods ):
        for mod in mods:
            self.append( mod )

class MinAggregateModifier( AggregateModifier ):
    def __init__( self, mods=None, target=None, type=None ):
        super( MinAggregateModifier, self ).__init__( mods, min, target, type )

class MaxAggregateModifier( AggregateModifier ):
    def __init__( self, mods=None, target=None, type=None ):
        super( MaxAggregateModifier, self ).__init__( mods, max, target, type )

class CappedAggregateModifier( AggregateModifier ):
    def __init__( self, cap, mods=None, target=None, type=None ):
        super( CappedAggregateModifier, self ).__init__( mods, lambda: min( cap, sum( self.mods ) ), target, type )

class ModifierFactory( MyObject ):
    def __init__( self, cause, number, name="" ):
        self.cause = cause
        self.targets = { }
        self.number = number
        self.targetId = None
        self.name = name
        self.static = False

    def __int__( self ):
        return self.number

    def __str__( self ):
        number = self.number
        name = self.name and " ( %s )" % self.name or self.name
        return "%s%s ( from %s%s )" % ( number > -1 and "+" or "", number, str( self.cause ), name )

    def addTarget( self, target, type, conditions=None, multiplier=1 ):
        if self.static:
            basemod = Modifier( type, self, target, conditions, self.number )
        else:
            basemod = Modifier( type, self, target, conditions )
        mod = MultipliedModifier( basemod, multiplier )
        try:
            self.targets[ target.key ].append( mod )
        except:
            self.targets[ target.key ] = [ mod ]
        target.modifiers[ mod.key ] = mod
        return mod

    def removeTarget( self, target ):
        del self.targets[ target.key ]
        del target.modifiers[ self.key ]

    #Properties
    def getKey( self ):
        return "%s: %s" % ( self.__class__.__name__, getattr( self.cause, 'key', self.cause ) )
    key = property( fget=getKey, doc="The unique key for this ModifierFactory" )

    def getNumber( self ):
        return self._number( )

    def setNumber( self, number ):
        self._number = callable( number ) and number or ( lambda: number )

    number = property( fget=getNumber, fset=setNumber, doc="This ModifierFactory's base value" )

class MultipliedModifierFactory( MyObject ):
    def __init__( self, factory, multiplier ):
        self.factory = factory
        self.multiplier = multiplier

    def __getattr__( self, attr ):
        return getattr( self.factory, attr )

    def addTarget( self, target, type, conditions=None ):
        return factory.addTarget( target, type, condition, self.multiplier )

    def removeTarget( self, target ):
        self.factory.removeTarget( target )

    def getMultiplier( self ):
        return self._multiplier( )
    
    def setMultiplier( self, val ):
        self._multiplier = callable( val ) and val or ( lambda: val )
    multiplier=property( fget=getMultiplier, fset=setMultiplier, doc="The multiplier function that will be applied to modifiers this generates" )

class LevelAggregator( AggregateModifier ):
    def append( self, level ):
        self.mods[ level.key ] = level

