from rep import *

class D20AbilityScore( Stat ):
    def __init__( self, name, number ):
        import math
        super( D20AbilityScore, self ).__init__( name, number, aggregator=MaxAggregateModifier )
        self.mod = lambda: int( math.floor( ( int( self ) - 10 ) / 2 ) )

class D20Attribute( Attribute ):
    def __init__( self, name, number ):
        super( D20Attribute, self ).__init__( name, number, aggregator=MaxAggregateModifier )

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
    def __init__( self, name, attrs=None ):
        super( D20Character, self ).__init__( name, attrs )
        self.FEATS = { }

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
                'INIT' : ( setAttribute, 'Initiative', ( ), 0 ),
                'SPEED' : ( setAttribute, 'Movement Speed', ( ), 30 ),
                'SIZE' : ( setSize, 'Size Category', ( ), 'M' )
                }

if __name__ == "__main__":
    sword = Weapon( 'Sword', [ 'MELEE', 'SLASHING', 'PIERCING', 'CORPORIAL' ] )
    bow = Weapon( 'Bow', [ 'RANGE', 'PIERCING', 'CORPORIAL' ] )
    grapple = Weapon( 'Grapple', [ 'MELEE', 'GRAPPLE', 'CORPORIAL' ] )
    bob = D20Character( "Bob", { 'STR': 13, 'DEX':15, 'CON':12, 'INT':10, 'WIS':8, 'CHA':18, 'HEIGHT':72, 'WEIGHT':221, 'WIDTH':24, 'DEPTH':12 } )
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
