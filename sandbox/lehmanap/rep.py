tabbies = ""

class MyObject( object ):
    def __repr__( self ):
        return "%s %s" % ( str( self ), super( MyObject, self ).__repr__( ) )

class Weapon( MyObject ):
    def __init__( self, name, types ):
        self.name = name
        self.TYPES = types

    def __str__( self ):
        return "%s %s" % ( self.name, self.TYPES )

class Situation( MyObject ):
    def __init__( self, subject, object, tool ):
        self.subject = subject
        self.object = object
        self.tool = tool

    def __str__( self ):
        "%s is doing something with %s using a(n) %s" % ( self, subject, self.object, self.tool )

class Attack( Situation ):
    def __str__( self ):
        "%s attacks %s using a(n) %s" % ( self, subject, self.object, self.tool )

class Condition( MyObject ):
    def __init__( self, attToCheck, valToCheck, partToCheck, op ):
        self.attToCheck = attToCheck.upper( )
        self.partToCheck = partToCheck.lower( )
        self.valToCheck = valToCheck.upper( )
        self.op = op.lower( )

    def check( self, circumstance ):
        try:
            vals = getattr( getattr( circumstance, self.partToCheck ), self.attToCheck, [ self.valToCheck ] )
            if self.op == "in":
                return self.valToCheck in vals
            elif self.op == "not in":
                return self.valToCheck not in vals
        except:
            return isinstance( circumstance, bool ) and circumstance
        
    def __str__( self ):
        return "( %s %s %s's %s )" % ( self.valToCheck, self.op, self.partToCheck, self.attToCheck )
        
class Conditions( MyObject ):
    def __init__( self, conditions, op ):
        self.conditions = [ ]
        for c in conditions:
            if isinstance( c, str ):
                c = c.split( )
                self.conditions.append( Condition( c[ -1 ], c[ 0 ], c[ -2 ], " ".join( c[ 1:-2 ] ) ) )
            elif isinstance( c, tuple ):
                self.conditions.append( Conditions( c[ :-1 ], c[ -1 ] ) )
        self.op = op.lower( )

    def __str__( self ):
        return ( " %s " % self.op ).join( [ str( c ) for c in self.conditions ] )
        
    def check( self, circumstance ):
        for c in self.conditions:
            truth = c.check( circumstance )
            if self.op == "and" and truth == False:
                return False
            elif self.op == "or" and truth == True:
                return True
        if self.op == "and":
            return True
        elif self.op == "or":
            return False


class Modifier( MyObject ):
    def __init__( self, parent, target, conditions ):
        self.parent = parent
        self.target = target
        self.conditions = conditions

    def __add__( self, other ):
        try:
            return int( self ) + other
        except:
            return other
    __radd__ = __add__

    def __int__( self ):
        if self.conditions.check( self.target.situation ):
        #If the circumstances are right, add me to the value
            return int( self.parent )
        else:
            raise "I don't modify %s under these circumstances" % self.target.name

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
        return self.parent.number
    number = property( fget=getNumber, doc="This Attributes base value" )

class MultipliedModifier( Modifier ):
    def __init__( self, mod, multiplier ):
        self.mod = mod
        self.multiplier = multiplier
    
    def __int__( self ):
        return self.multiplier * int( self.mod )
    
    def __str__( self ):
        try:
            if self.multiplier != 1:
                return "%s = %s x %s" % ( int( self ), str( self.mod ), self.multiplier )
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

class ModifierFactory( MyObject ):
    def __init__( self, cause, number, name="" ):
        self.cause = cause
        self.targets = { }
        self.number = number
        self.targetId = None
        self.name = name

    def __int__( self ):
        return self.number

    def __str__( self ):
        number = self.number
        name = self.name and " ( %s )" % self.name or self.name
        return "%s%s ( from %s%s )" % ( number > -1 and "+" or "", number, str( self.cause ), name )

    def addTarget( self, target, conditions=None ):
        self.addMultipliedTarget( target, 1, conditions )

    def addMultipliedTarget( self, target, multiplier, conditions=None ):
        conditions = conditions or Conditions( ( ), "and" )
        mod = MultipliedModifier( Modifier( self, target, conditions ), multiplier )
        try:
            self.targets[ target.key ].append( mod )
        except:
            self.targets[ target.key ] = [ mod ]
        try:
            target.modifiers[ self.key ].append( mod )
        except:
            target.modifiers[ self.key ] = [ mod ]

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

class Attribute( MyObject ):
    lastkey = 0
    
    def __init__( self, name, number ):
        self.name = name
        self.number = number
        self.modifiers = { }
        self.key = "%s %s" % ( self.__class__.__name__, self.lastkey )
        Attribute.lastkey += 1
        self.situation = True

    def __add__( self, other ):
        return int( self ) + other
    __radd__ = __add__

    def __cmp__( self, other ):
        import math
        diff = self - other
        return diff and diff / math.fabs( diff ) or diff

    def __int__( self ):
        mods = [ ]
        vals = [ ]
        for m in self.modifiers.values( ):
            try:
                mods.extend( m )
            except TypeError:
                mods.append( m )
        for m in mods:
            try:
                vals.append( int( m ) )
            except:
                pass
        return self.number + sum( vals )

    def __neg__( self ):
        return -int( self )

    def __str__( self ):
        mods = [ ]
        for m in self.modifiers.values( ):
            try:
                mods.extend( m )
            except TypeError:
                mods.append( m )
        fixings = ""
        global tabbies
        tabbies += "\t"
        for x in [ self.number ] + [ mod for mod in mods ]:
            s = str( x )
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
    def __init__( self, name, number, modprovided=None ):
        super( Stat, self ).__init__( name, number )
        self.mod = modprovided or self.number

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
            for modStr, targetCondition in targetStrs.iteritems( ):
                tags = modStr.split( )
                target = self.attrs[ tag ]
                mod = self.attrs[ tags[ -1 ] ].mod
                if len( targetCondition ) > 0:
                    condition = Conditions( targetCondition[ :-1 ], targetCondition[ -1 ] )
                else:
                    condition = Conditions( ( ), "and" )
                if len( tags ) > 1:
                    mod.addMultipliedTarget( target, int( tags[ 0 ] ), condition )
                else:
                    mod.addTarget( target, condition )

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
            mod.addTarget( self.typerefs[ type ].attrs[ target ] )

    def applyMods( self, type ):
        for target, mod in self.modsprovided[ type ].items( ):
            mod.addTarget( self.typerefs[ type ].attrs[ target ] )

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

    def __init__( self, name, attrs=None ):
        self.name = name
        self.attrs = { }
        self.key = "%s %s" % ( self.__class__.__name__, self.lastkey )
        self.equipment = { }
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

if __name__ == "__main__":
    import math
    STR = Stat( "Strength", 14, conditions )
    bob = Character( "Bob", conditions )
