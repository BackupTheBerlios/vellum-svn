from wrapper import Condition, MyObject
from attribute import Attribute, Stat
from modifier import AggregateModifier, Modifier, ModifierFactory

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
