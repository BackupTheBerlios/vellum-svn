import pdb
tabbies = ""

class Observer( object ):
    def __init__( self, label ):
        self.label = label

    def observed( self, obj, function ):
        print "%s observed %s" % ( self.label, function )

class ObservedMethod( object ):
    def __init__( self, meth ):
        self.method = meth
        self.observers = [ ]

    def __call__( self, *args, **kwargs ):
        for observer in self.observers:
            observer.observed( self.method )
        return self.method( *args, **kwargs )

    def add( self, observer ):
        self.observers.append( observer )

class ConditionalMethod( object ):
    def __init__( self, methods, conditionType ):
        try:
            self.method, self.altmethod = methods
        except:
            self.method, self.altmethod = [ methods, ( lambda *args, **kwargs: 0 ) ]
        self.condition = conditionType( )

    def __call__( self, *args, **kwargs ):
        return self.condition and self.method( *args, **kwargs ) or self.altmethod( *args, **kwargs )

    def add( self, condition ):
        try:
            self.condition.extend( condition )
        except:
            self.condition.append( condition )

class AndConditionalMethod( ConditionalMethod ):
    def __init__( self, meth ):
        super( AndConditionalMethod, self ).__init__( meth, AndCondition )

class OrConditionalMethod( ConditionalMethod ):
    def __init__( self, meth ):
        super( AndConditionalMethod, self ).__init__( meth, OrCondition )

class Wrappable( object ):
    def __init__( self, func, returntype=ObservedMethod ):
        self.func = func
        self.wrapped = { }
        self.returntype = returntype

    def __get__( self, obj, objtype=None ):
        if obj is None:
            return self.func
        return self.wrapped[ obj ]
    
    def __set__( self, obj, newfunc ):
        if obj is None:
            self.func = newfunc
        self.wrapped[ obj ] = self.returntype( newfunc )
    
    def __delete__( self, obj ):
        if obj is None:
            del self.func
        del self.wrapped[ obj ]

    def get__doc__( self ):
        return self.func.__doc__
    __doc__ = property( fget=get__doc__ )

class Observable( Wrappable ):
    def __init__( self, func ):
        super( Observable, self ).__init__( func, ObservedMethod )

class Conditionable( Wrappable ):
    def __init__( self, func, conditionalType=None ):
        conditionalType=conditionalType or AndCondition
        wrappertype = ( lambda meth, conditionalType=conditionalType: ConditionalMethod( meth, conditionalType ) )
        super( Conditionable, self ).__init__( func, wrappertype )

class WrappableObject( object ):
    def __new__( clss, *args, **kwargs ):
        obj = object.__new__( clss, *args, **kwargs )
        for methname, meth in [ ( m, getattr( clss, m ) ) for m in dir( clss ) if callable( getattr( clss, m ) ) ]:
            import new
            try:
                setattr( obj, methname, new.instancemethod( meth, obj, clss ) )
            except TypeError:
                pass
        return obj

class MyObject( WrappableObject ):
    def __str__( self ):
        return "%s.%s" % ( self.__class__.__module__, self.__class__.__name__ )

    def __repr__( self ):
        return "%s %s" % ( str( self ), super( MyObject, self ).__repr__( ) )

class Condition( MyObject, Observer ):
    def __init__( self, func=None ):
        self.func = func or ( lambda: True )

    def observed( self, func ):
        return self.func( func )

class MassCondition( Condition ):
    def __init__( self, conditions=None ):
        self.conditions = [ condition for condition in ( conditions or [ ] ) ]

    def __iter__( self ):
        return iter( self.conditions )

    def append( self, condition ):
        self.conditions.append( condition )

    def extend( self, conditions ):
        self.conditions.extend( conditions )

class AndCondition( MassCondition ):
    def observed( self, meth ):
        for condition in self.conditions:
            if not condition( meth.im_self, meth ):
                return False
        return True

class OrCondition( MassCondition ):
    def observed( self, meth ):
        for condition in self.conditions:
            if condition( meth.im_self, meth ):
                return True
        return False

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

class GameObjectMetaclass( type ):
    def __init__( clss, name, bases, dictionary ):
        def generateProperty( attrType, attrTag, attrName ):
            """
            Because lambdas do not rememebr their scope, if the stack is overwritten.
            """
            return ( lambda self: self.attrs[ attrTag ] ), ( lambda self, value: attrType( self, attrTag, attrName, value ) )

        for attrTag, ( attrType, attrName, attrLinks, baseVal ) in clss.attTypes.items( ):
            get, set = generateProperty( attrType, attrTag, attrName )
            prop = property( fget=get, fset=set, doc="This character's %s score" % attrName )
            setattr( clss, attrTag, prop )
        super( GameObjectMetaclass, clss ).__init__( clss, name, bases, dictionary )

class GameObject( MyObject ):
    def __init__( self, attrs ):
        self.setAttrs( attrs or { } )
        self.setSystemAttrs( )

    def setAttrs( self, attrs ):
        classattrs = dict( [ ( key, baseVal ) for key, ( attType, attName, targetStrs, baseVal ) in self.attTypes.iteritems( ) ] )
        classattrs.update( attrs )
        for name, attr in classattrs.items( ):
            setattr( self, name, attr )

    def setSystemAttrs( self ):
        for tag, ( attType, attName, targetStrs, baseVal ) in self.attTypes.iteritems( ):
            try:
                for ( type, source, targetCondition ) in targetStrs:
                    tags = source.split( )
                    target = self.attrs[ tag ]
                    mod = self.attrs[ tags[ -1 ] ].mod
                    condition = Condition( targetCondition )
                    if len( tags ) > 1:
                        mod.addTarget( target, type, condition, int( tags[ 0 ] ) )
                    else:
                        mod.addTarget( target, type, condition )
            except ValueError, e:
                import pdb
                pdb.set_trace( )
                raise e

    #Properties
    def setAttribute( self, tag, name, number ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = Attribute( name, number )

    def setStat( self, tag, name, number, modprovided=None ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = Stat( name, number, modprovided )

    attTypes = { 
                'WEIGHT' : ( setAttribute, 'Weight', { }, 1 ),
                'HEIGHT' : ( setAttribute, 'Height', { }, 1 ),
                'WIDTH' : ( setAttribute, 'Width', { }, 1 ),
                'DEPTH' : ( setAttribute, 'Depth', { }, 1 ),
                }

    __metaclass__ = GameObjectMetaclass

class Item( GameObject ):
    lastkey = 0

    def __init__( self, name, cost, attrs, description, mods ):
        self.name = name
        self.attrs = { }
        self.cost = cost
        self.description = description
        super( Item, self ).__init__( attrs )
        self.modsprovided = { 'CARRIER': { 'WEIGHT': self.WEIGHT.mod } }
        self.typerefs = { 'CARRIER': None }
        self.key = "%s %s" % ( self.__class__.__name__, self.lastkey )
        Item.lastkey += 1
        self.setMods( mods )

    def __str__( self ):
        return self.name

    def addMod( self, mod, type, target ):
        self.modsprovided[ type ][ target ] = mod
        if self.typerefs[ type ]:
            mod.addTarget( self.typerefs[ type ].attrs[ target ], type )

    def applyMods( self, type ):
        for target, mod in self.modsprovided[ type ].items( ):
            mod.addTarget( self.typerefs[ type ].attrs[ target ], type )

    def revokeMods( self, type ):
        for target, mod in self.modsprovided[ type ].items( ):
            mod.removeTarget( self.typerefs[ type ].attrs[ target ] )

    def beCarried( self, carrier ):
        self.carrier = carrier
        self.applyMods( 'CARRIER' )

    def beDropped( self ):
        self.revokeMods( 'CARRIER' )
        self.carrier = None

    def setMods( self, mods ):
        for modType, modifiers in mods.items( ):
            for target, ( number, name ) in modifiers.items( ):
                self.addMod( ModifierFactory( self, number, name ), modType, target )

    #Properties
    def getCarrier( self ):
        return self.typerefs[ 'CARRIER' ]

    def setCarrier( self, value ):
        self.typerefs[ 'CARRIER' ] = value
    carrier = property( fget=getCarrier, fset=setCarrier, doc="The character carrying this Item." )

    attTypes = { 
                'WEIGHT' : ( GameObject.setStat, 'Weight', { }, 1 ),
                'HEIGHT' : ( GameObject.setStat, 'Height', { }, 1 ),
                'WIDTH' : ( GameObject.setStat, 'Width', { }, 1 ),
                'DEPTH' : ( GameObject.setStat, 'Depth', { }, 1 ),
                }

class EquippedItem( Item ):
    def __init__( self, *args, **kwargs ):
        super( EquippedItem, self ).__init__( *args, **kwargs )
        self.typerefs[ 'EQUIPPER' ] = { }

    #Properties
    def getEquipper( self ):
        return self.typerefs[ 'EQUIPPER' ]

    def setEquipper( self, value ):
        self.typerefs[ 'EQUIPPER' ] = value
    equipper = property( fget=getEquipper, fset=setEquipper, doc="The Character that has equipped this item." )

class Character( GameObject ):
    lastkey = 0
    aggregator = None

    def __init__( self, name, attrs=None ):
        self.name = name
        self.attrs = { }
        self.key = "%s %s" % ( self.__class__.__name__, self.lastkey )
        self.equipment = { }
        self.effects = [ ]
        Character.lastkey += 1
        super( Character, self ).__init__( attrs )

    def __str__( self ):
        return "%s\n\t%s\n" % ( self.name, "\n\t".join( [ str( attr ) for attr in self.attrs.values( ) ] ) )

    def carry( self, item ):
        self.equipment[ item.key ] = item
        item.beCarried( self )

    def drop( self, item ):
        del self.equipment[ item.key ]
        item.beDropped( )

    attTypes = { }

class EffectGenerator( MyObject ):
    def __init__( self, name, session, mods=None, feats=None, effecttype=None ):
        super( EffectGenerator, self ).__init__( )
        self.name = name
        self.mods = mods
        self.feats = feats
        self.session = session
        self.effecttype = effecttype

    def getEffect( self, character, newmods=None ):
        mods = self.mods.copy( )
        newmods = newmods or { }
        mods.update( newmods )
        for target, mod in mods.items( ):
            mods[ target ] = ( 'RANKS', Condition( ), mod )
        return self.effecttype( character, self, mods, self.feats )

    def __str__( self ):
        return self.name

class LevelGenerator( MyObject ):
    def __init__( self, name, session, levels, mods, feats, effecttype ):
        super( LevelGenerator, self ).__init__( )
        self.name = name
        self.session = session
        mods = [ dict( [ ( key, vals[ i ] ) for key, vals in mods.items( ) ] ) for i in range( levels ) ]
        feats = [ dict( [ ( key, vals[ i ] ) for key, vals in feats.items( ) ] ) for i in range( levels ) ]
        self.levels = [ ]
        for number, ( mod, feat ) in enumerate( zip( mods, feats ) ):
            genfunc = lambda character, generator, mods, feats, number=number+1: effecttype( character, number, character.level, mods, feats )
            self.levels.append( EffectGenerator( name, session, mod, feat, genfunc ) )

    def getLevel( self, character, number ):
        return self.levels[ number ].getEffect( character )

    def __str__( self ):
        return self.name

class CharacterClass( LevelGenerator ):
    def __init__( self, name, session, levels, mods, feats ):
        genfunc = lambda character, classlevel, charlevel, mods, feats: CharacterLevel( character, classlevel, charlevel, self, mods, feats )
        super( CharacterClass, self ).__init__( name, session, levels, mods, feats, genfunc )

class Race( LevelGenerator ):
    def __init__( self, name, session, levels, mods, feats ):
        genfunc = lambda character, classlevel, charlevel, mods, feats: RaceLevel( character, classlevel, charlevel, self, mods, feats )
        super( Race, self ).__init__( name, session, levels, mods, feats, genfunc )

    def getLevel( self, character, number, charclass ):
        #When we have Unknowns, this will be used to hook the races UnknownSkills
        #to the class level being gained
        return super( Race, self ).getLevel( character, number )

class LevelAggregator( AggregateModifier ):
    def append( self, level ):
        self.mods[ level.key ] = level

class Effect( MyObject ):
    def __init__( self, character, mods=None, feats=None ):
        super( Effect, self ).__init__( )
        self.character = character
        self.enabled = True
        mods = mods or {}
        self.modifiers = { }
        self.factories = { }
        for key, ( type, conditions, number ) in mods.items( ):
            target = getattr( character, key )
            factory = ModifierFactory( self, number, '%s Modifier' % self.__class__.__name__ )
            self.factories[ target ] = ( factory, type, conditions )
        self.feats = feats or { }

    def __lt__( self, other ):
        return self.charlevelnum < other.charlevelnum

    def __str__( self ):
        return self.__class__.__name__

    def enable( self ):
        if not self.modifiers:
            for target, ( factory, type, conditions ) in self.factories.items( ):
                self.modifiers[ target ] = factory.addTarget( target, type, conditions )
        else:
            for target, mod in self.modifiers.items( ):
                target.modifiers[ mod.key ] = mod
        self.enabled = True

    def disable( self ):
        for target, ( factory, type, conditions ) in self.factories.items( ):
            factory.removeTarget( target )
        self.enabled = False

    #Properties
    def getKey( self ):
        return hash( self )
    key = property( fget=getKey, doc="Unique Key" )

class Level( Effect ):
    def __init__( self, character, levelnum, charlevelnum, mods=None, feats=None ):
        super( Level, self ).__init__( character, mods, feats )
        self.levelnum = levelnum + 1
        self.charlevelnum = charlevelnum

    def __int__( self ):
        if self.enabled:
            return 1
        else:
            return 0

class DamageEffect( Effect ):
    def __init__( self, character, attack, mods=None, effects=None ):
        self.attack = attack
        super( DamageEffect, self ).__init__( character, mods, effects )

    def __str__( self ):
        return "%s %s" % ( super( DamageEffect, self ).__str__( ), 0 )

class CharacterLevel( Level ):
    def __init__( self, character, levelnum, charlevelnum, characterclass, mods=None, feats=None ):
        self.characterclass = characterclass
        super( CharacterLevel, self ).__init__( character, levelnum, charlevelnum, mods, feats )

    def __str__( self ):
        if self.enabled:
            return  "%s %s, %s/%s" % ( self.type, self.levelnum, self.charlevelnum, int( self.character.levels ) )
        else:
            return "\b"

    #Properties
    def getType( self ):
        return self.characterclass.name
    type = property( fget=getType, doc="The Class assosciated with this level." )

class RaceLevel( Level ):
    def __init__( self, character, levelnum, charlevelnum, racename, mods=None, feats=None ):
        self.racename = racename
        super( RaceLevel, self ).__init__( character, levelnum, charlevelnum, mods, feats )
    def __int__( self ):
        return 0

    def __str__( self ):
        if self.enabled:
            return  "%s %s, %s/%s" % ( self.racename, self.levelnum, self.charlevelnum, int( self.character.levels ) )
        else:
            return "\b"

    #Properties
    def getType( self ):
        return 'RACE'
    type = property( fget=getType )

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

if __name__ == "__main__":
    import math
    STR = Stat( "Strength", 14, conditions )
    bob = Character( "Bob", conditions )
