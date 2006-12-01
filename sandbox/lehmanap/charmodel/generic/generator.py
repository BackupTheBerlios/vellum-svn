from wrapper import Condition, MyObject
from effect import CharacterLevel, RaceLevel

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
            genfunc = lambda character, generator, mods, feats, number=number: effecttype( character, number, character.level, mods, feats )
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
