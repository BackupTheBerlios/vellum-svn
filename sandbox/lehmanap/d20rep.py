from rep import *

class LevelAggregator( AggregateModifier ):
    def append( self, level ):
        self.mods[ level.key ] = level

class Level( MyObject ):
    def __init__( self, character, levelnum, charlevelnum, mods=None, feats=None ):
        self.character = character
        self.levelnum = levelnum + 1
        self.charlevelnum = charlevelnum
        self.enabled = True
        self.factories = { }
        mods = mods or {}
        for key, ( type, conditions, number ) in mods.items( ):
            if isinstance( conditions, tuple ):
                conditions = Constitution.compileCondition( conditions )
            target = getattr( character, key )
            factory = ModifierFactory( self, number, 'Level Modifier' )
            self.factories[ target ] = ( factory, type, conditions )
        self.feats = feats or { }

    def enable( self ):
        for target, ( factory, type, conditions ) in self.factories.items( ):
            factory.addTarget( target, type, conditions )
        self.enabled = True

    def disable( self ):
        for target, ( factory, type, conditions ) in self.factories.items( ):
            factory.removeTarget( target )
        self.enabled = False

    def __int__( self ):
        if self.enabled:
            return 1
        else:
            return 0

    #Properties
    def getKey( self ):
        return hash( self )
    key = property( fget=getKey, doc="Unique Key" )

    def __lt__( self, other ):
        return self.charlevelnum < other.charlevelnum

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

class D20LevelGenerator( MyObject ):
    def __init__( self, name, session, mods, feats, leveltype ):
        super( D20LevelGenerator, self ).__init__( )
        self.name = name
        self.mods = mods
        self.feats = feats
        self.session = session
        self.leveltype = leveltype

    def getLevel( self, character, number ):
        mods = { }
        try:
            charlevelnum = 1
            for level in character.levels[ 'RACE' ].values( ):
                if level.enabled:
                    charlevelnum += 1
        except KeyError:
            charlevelnum = 1
        for key, mod in self.mods.items( ):
            mods[ key ] = ( 'RANKS', Conditions( ( ), "and" ), mod[ number ] )
        return self.leveltype( character, number, charlevelnum, self, mods, self.feats )

    def __str__( self ):
        return self.name

class D20CharacterClass( D20LevelGenerator ):
    def __init__( self, name, session, mods, feats ):
        super( D20CharacterClass, self ).__init__( name, session, mods, feats, CharacterLevel )

class D20Race( D20LevelGenerator ):
    def __init__( self, name, session, mods, feats ):
        super( D20Race, self ).__init__( name, session, mods, feats, RaceLevel )

    def getLevel( self, character, number, charclass ):
        #When we have Unknowns, this will be used to hook the races UnknownSkills
        #to the class level being gained
        return super( D20Race, self ).getLevel( character, number )

class D20AbilityScore( Stat ):
    def __init__( self, name, number ):
        import math
        super( D20AbilityScore, self ).__init__( name, number, aggregator=MaxAggregateModifier )
        self.mod = lambda: int( math.floor( ( int( self ) - 10 ) / 2 ) )
        self.modifiers[ 'INNATE' ] = CappedAggregateModifier( 5, target=self )
        self.modifiers[ 'RANKS' ] = AggregateModifier( target=self )

class D20Skill( Stat ):
    def __init__( self, name, number ):
        super( D20Skill, self ).__init__( name, number, aggregator=MaxAggregateModifier )
        self.modifiers[ 'INNATE' ] = CappedAggregateModifier( 5, target=self )
        self.modifiers[ 'RANKS' ] = AggregateModifier( target=self )

class D20Attribute( Attribute ):
    def __init__( self, name, number ):
        super( D20Attribute, self ).__init__( name, number, aggregator=MaxAggregateModifier )
        self.modifiers[ 'INNATE' ] = CappedAggregateModifier( 5, target=self )
        self.modifiers[ 'RANKS' ] = AggregateModifier( target=self )

class D20Size( Stat ):
    def __init__( self, magnitude ):
        if isinstance( magnitude, D20Size ):
            magnitude = magnitude.magnitude
        elif isinstance( magnitude, str ):
            magnitude = dict( [ ( val, key ) for key, val in self.sizeRanks.items( ) ] )[ magnitude ]
        super( D20Size, self ).__init__( 'Size', magnitude, self.__int__ )

    def __add__( self, other ):
        return D20Size( self.number + other )
    __radd__ = __add__

    def __sub__( self, other ):
        return D20Size( self.number - other )
    __rsub__ = __sub__

    def __int__( self ):
        try:
            magnitude = super( D20Size, self ).__int__( )
            absval = abs( magnitude )
            vector = magnitude/ absval
            return ( 2 ** ( absval - 1 ) ) * vector
        except:
            return 0

    def __str__( self ):
        try:
            category = self.sizeRanks[ super( D20Size, self ).__int__( ) ]
            category = "%s (%s)" % ( category, self.sizeNames[ category ] )
        except:
            category = "No category for this size"
        return "%s %s" % ( super( D20Size, self ).__str__( ), category )

    #Properties
    def getLetter( self ):
        return self.sizeRanks[ self.number ]
    letter = property( fget=getLetter, doc="The letter of this size" )

    sizeRanks = { -3:'F', -2:'T', -1:'S', 0:'M', 1:'L', 2:'H', 3:'C', 4:'G', }
    sizeNames = { 'F':"Fine", 'T':"Tiny", 'S':"Small", 'M':"Medium", 'L':"Large", 'H':"Huge", 'C':"Collosal", 'G':"Gargantuan" }

class D20Character( Character ):
    def __init__( self, name, race, attrs=None ):
        super( D20Character, self ).__init__( name, attrs )
        self.levels = LevelBox( )
        self.race = race
        self.FEATS = { }

    def addLevel( self, characterclass ):
        try:
            numlevels = int( self.levels[ characterclass.name ] )
        except KeyError:
            numlevels = 0
        classlevel = characterclass.getLevel( self, numlevels )
        racelevel = self.race.getLevel( self, numlevels, characterclass )
        self.levels.addLevel( classlevel )
        self.levels.addLevel( racelevel )
        classlevel.enable( )
        racelevel.enable( )

    def beginCombat( self ):
        self.DEX.mod.addTarget( self.AC, 'ATTRIBUTE', Conditions( ( ), "and" ) )

    def endCombat( self ):
        self.DEX.mod.removeTarget( self.AC )

    def attack( self, foe, weapon ):
        #This will need fixing.  It's just for testing purposes.  FIXME
        self.ATT.situation = Attack( self, foe, weapon )

    def unreadyWeapon( self ):
        #This will need fixing.  It's just for testing purposes.  FIXME
        unarmed = Weapon( 'Unarmed', [ 'MELEE', 'UNARMED', 'BLUDGEON', 'CORPORIAL' ] )
        self.ATT.situation = unarmed

    #Properties
    def setAbilityScore( self, tag, name, number, modsprovided=None ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = D20AbilityScore( name, number )

    def setAttribute( self, tag, name, number ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = D20Attribute( name, number )

    def setSize( self, tag, name, letter, modsprovided=None ):
        try:
            self.attrs[ tag ].letter = letter
        except:
            self.attrs[ tag ] = D20Size( letter )

    attTypes = { 
                #Basic Attributes
                'STR' : ( setAbilityScore, 'Strength', ( ), 0 ),
                'DEX' : ( setAbilityScore, 'Dexterity', ( ), 0 ),
                'CON' : ( setAbilityScore, 'Constitution', ( ), 0 ),
                'INT' : ( setAbilityScore, 'Intelligence', ( ), 0 ),
                'WIS' : ( setAbilityScore, 'Wisdom', ( ), 0 ),
                'CHA' : ( setAbilityScore, 'Charisma', ( ), 0 ),
                #END Basic Attributes

                #Calculated Attributes
                'AC' : ( setAttribute, 'Armor Class', 
                    (
                        ( 'SIZE', '-1 SIZE', ( ) ),
                    ), 10 ),
                'ATT' : ( setAttribute, 'Attack Bonus', 
                    (
                        ( 'ABILITY', 'STR', ( "MELEE IN TOOL TYPES", ( "WPN_FINESSE NOT IN SUBJECT FEATS", "FINESSABLE NOT IN TOOL TYPES", "or" ), "and" ) ),
                        ( 'ABILITY', 'DEX', ( "RANGE IN TOOL TYPES", "and" ) ),
                        ( 'SIZE', 'SIZE', ( "GRAPPLE IN TOOL TYPES", "and" ) ),
                        ( 'SIZE', '-1 SIZE', ( "GRAPPLE NOT IN TOOL TYPES", "and" ) ),
                    ), -4 ),
                'WILL' : ( setAttribute, 'Will Save', 
                    (
                        ( 'ABILITY', 'WIS', ( ) ),
                    ), 0 ),
                'FORT' : ( setAttribute, 'Fortitude Save', 
                    (
                        ( 'ABILITY', 'CON', ( ) ),
                    ), 0 ),
                'REF' : ( setAttribute, 'Reflex Save', 
                    (
                        ( 'ABILITY', 'DEX', ( ) ),
                    ), 0 ),
                'INIT' : ( setAttribute, 'Initiative', ( ), 0 ),
                'SPEED' : ( setAttribute, 'Movement Speed', ( ), 30 ),
                'SIZE' : ( setSize, 'Size Category', ( ), 'M' )
                }

if __name__ == "__main__":
    sword = Weapon( 'Sword', [ 'MELEE', 'SLASHING', 'PIERCING', 'CORPORIAL' ] )
    bow = Weapon( 'Bow', [ 'RANGE', 'PIERCING', 'CORPORIAL' ] )
    grapple = Weapon( 'Grapple', [ 'MELEE', 'GRAPPLE', 'CORPORIAL' ] )
    race = D20Race( 'Elf', None, 
                {
                    'DEX': [ 2 ] + [ 0 ] * 19,
                    'CON': [ -2 ] + [ 0 ] * 19
                }, { } )
    bob = D20Character( "Bob", race, { 'STR': 13, 'DEX':15, 'CON':12, 'INT':10, 'WIS':8, 'CHA':18, 'HEIGHT':72, 'WEIGHT':221, 'WIDTH':24, 'DEPTH':12 } )
    charclass = D20CharacterClass( 'Fighter', None, 
                { 
                    'ATT': [ 1 ] * 20,
                    'FORT': ( [ 2 ] + [ 1, 0 ] * 10 )[ :20 ],
                    'WILL': ( [ 0, 0, 1 ] * 7 )[ :20 ],
                    'REF': ( [ 0, 0, 1 ] * 7 )[ :20 ]
                }, { } )
    print int( bob.levels )
    bob.addLevel( charclass )
    print bob.levels
    print bob.ATT
    bob.addLevel( charclass )
    print bob.levels
    print bob.ATT
    print "AC before Dex mod"
    print bob.AC
    bob.beginCombat( )
    print "After"
    print bob.AC
    print "ATT before weapon"
    bob.unreadyWeapon( )
    print int( bob.ATT )
    bob.attack( bob, sword )
    print "After Sword"
    print int( bob.ATT )
    bob.unreadyWeapon( )
    print "Sword Removed"
    print int( bob.ATT )
    bob.attack( bob, bow )
    print "With Bow"
    print bob.ATT
    strstone = Item( 'Strength Stone', 0, { 'WEIGHT':5, 'HEIGHT':6, 'WIDTH':6, 'DEPTH':6 }, 'A plain round stone', { 'CARRIER' : { 'STR' : ( 2, '' ) } } )
    strstone2 = Item( 'Strength Stone2', 0, { 'WEIGHT':5, 'HEIGHT':6, 'WIDTH':6, 'DEPTH':6 }, 'A plain round stone', { 'CARRIER' : { 'STR' : ( 5, '' ) } } )
    bob.unreadyWeapon( )
    print "Sword + Strength Stone"
    bob.attack( bob, sword )
    bob.carry( strstone )
    print bob.ATT
    bob.unreadyWeapon( )
    print "Sword + Strength Stone + Strength Stone 2"
    bob.attack( bob, sword )
    bob.carry( strstone2 )
    print bob.ATT
    bob.unreadyWeapon( )
    bob.attack( bob, grapple )
    print "Grappling"
    print int( bob.ATT )
    print bob.WILL
    print bob.FORT
    print bob.REF
