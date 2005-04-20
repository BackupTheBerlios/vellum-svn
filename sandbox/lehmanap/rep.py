conditions = { True: lambda a: True }
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
        vals = getattr( getattr( circumstance, self.partToCheck ), self.attToCheck, [ self.valToCheck ] )
        if self.op == "in":
            return self.valToCheck in vals
        elif self.op == "not in":
            return self.valToCheck not in vals
        
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

class ModifierFactory( MyObject ):
    def __init__( self, cause, number ):
        self.cause = cause
        self.targets = { }
        self.number = number
        self.targetId = None

    def __int__( self ):
        return self.number

    def __str__( self ):
        number = self.number
        return "%s%s ( from %s )" % ( number > -1 and "+" or "", number, str( self.cause ) )

    def addTarget( self, target, conditions ):
        mod = Modifier( self, target, conditions )
        self.targets[ target.key ] = mod
        target.modifiers[ self.key ] = mod

    def removeTarget( self, target ):
        del self.targets[ target.key ]
        del target.modifiers[ self.key ]

    #Properties
    def getKey( self ):
        return "%s: %s %s" % ( self.__class__.__name__, getattr( self.cause, 'key', self.cause ), " ".join( self.targets.keys( ) ) )
    key = property( fget=getKey, doc="The unique key for this ModifierFactory" )
    
    def getNumber( self ):
        return self._number( )

    def setNumber( self, number ):
        self._number = callable( number ) and number or ( lambda: number )

    number = property( fget=getNumber, fset=setNumber, doc="This Attributes base value" )

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
        return self.number + sum( self.modifiers.values( ) )

    def __str__( self ):
        return "%s: " % self.name + " ".join( [ "%s" % self.number ] + [ str( mod ) for mod in self.modifiers.values( ) ] ) + " = %s" % int( self )

    def __sub__( self, other ):
        return int( self ) - other
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

    number = property( fget=getNumber, fset=setNumber, doc="This Attributes base value" )

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

class CharacterMetaclass( type ):
    def __init__( clss, name, bases, dictionary ):
        def generateProperty( attrType, attrTag, attrName ):
            """
            Because lambdas do not rememebr their scope, if the stack is overwritten.
            """
            return ( lambda self: self.attrs[ attrTag ] ), ( lambda self, value: attrType( self, attrTag, attrName, value ) )

        for attrTag, ( attrType, attrName, attrLinks, baseVal ) in clss.attTypes.items( ):
            get, set = generateProperty( attrType, attrTag, attrName )
            prop = property( fget=get, fset=set, doc="This character's %s scor" % attrName )
            setattr( clss, attrTag, prop )
        super( CharacterMetaclass, clss ).__init__( clss, name, bases, dictionary )

class Character( MyObject ):
    lastkey = 0

    def __init__( self, name, attrs=None ):
        self.name = name
        self.attrs = { }
        self.key = "%s %s" % ( self.__class__.__name__, self.lastkey )
        Character.lastkey += 1
        self.setAttrs( attrs or { } )
        self.setSystemAttrs( )

    def setAttrs( self, attrs ):
        classattrs = dict( [ ( key, baseVal ) for key, ( attType, attName, targetStrs, baseVal ) in self.attTypes.iteritems( ) ] )
        classattrs.update( attrs )
        for name, attr in classattrs.items( ):
            setattr( self, name, attr )

    def setSystemAttrs( self ):
        """
        Set the attributes that are specific to the system.  Since this is generic, we'll pass
        """
        for tag, ( attType, attName, targetStrs, baseVal ) in self.attTypes.iteritems( ):
            for modStr, targetCondition in targetStrs.iteritems( ):
                target = self.attrs[ tag ]
                mod = self.attrs[ modStr ].mod
                if len( targetCondition ) > 0:
                    condition = Conditions( targetCondition[ :-1 ], targetCondition[ -1 ] )
                else:
                    condition = Conditions( ( ), "and" )
                mod.addTarget( target, condition )

    def __str__( self ):
        return "%s\n\t%s\n" % ( self.name, "\n\t".join( [ str( attr ) for attr in self.attrs.values( ) ] ) )

    #Properties
    def setStat( self, tag, name, number, modprovided=None ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = Stat( name, number, modprovided )

    def setAttribute( self, tag, name, number ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = Attribute( name, number )

    attTypes = { }
    __metaclass__ = CharacterMetaclass

if __name__ == "__main__":
    import math
    STR = Stat( "Strength", 14, conditions )
    bob = Character( "Bob", conditions )
