from wrapper import MyObject
from modifier import AggregateModifier, Modifier, ModifierFactory, MultipliedModifier

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


