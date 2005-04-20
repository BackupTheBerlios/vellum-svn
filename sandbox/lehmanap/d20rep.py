from rep import *

class D20AbilityScore( Stat ):
    def __init__( self, name, number ):
        import math
        super( D20AbilityScore, self ).__init__( name, number )
        self.mod = lambda: int( math.floor( ( int( self ) - 10 ) / 2 ) )

class D20Character( Character ):
    def __init__( self, name, attrs=None ):
        super( D20Character, self ).__init__( name, attrs )
        self.FEATS = { }

    def beginCombat( self ):
        self.DEX.mod.addTarget( self.AC, Conditions( ( ), "and" ) )

    def endCombat( self ):
        self.DEX.mod.removeTarget( self.AC )

    def attack( self, foe, weapon ):
        #This will need fixing.  It's just for testing purposes.  FIXME
        self.ATT.situation = Attack( self, foe, weapon )

    def unreadyWeapon( self ):
        #This will need fixing.  It's just for testing purposes.  FIXME
        self.ATT.situation = None

    #Properties
    def setAbilityScore( self, tag, name, number, modsprovided=None ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = D20AbilityScore( name, number )

    attTypes = { 
                #Basic Attributes
                'STR' : ( setAbilityScore, 'Strength', { }, 0 ),
                'DEX' : ( setAbilityScore, 'Dexterity', { }, 0 ),
                'CON' : ( setAbilityScore, 'Constitution', { }, 0 ),
                'INT' : ( setAbilityScore, 'Intelligence', { }, 0 ),
                'WIS' : ( setAbilityScore, 'Wisdom', { }, 0 ),
                'CHA' : ( setAbilityScore, 'Charisma', { }, 0 ),
                #END Basic Attributes

                #Calculated Attributes
                'AC' : ( Character.setAttribute, 'Armor Class', { }, 10 ),
                'ATT' : ( Character.setAttribute, 'Attack Bonus', 
                    { 
                        'STR': ( "MELEE IN TOOL TYPES", "WPN_FINESSE NOT IN SUBJECT FEATS", "and" ),
                        'DEX': ( "RANGE IN TOOL TYPES", "WPN_FINESSE NOT IN SUBJECT FEATS", "and" )
                    }, -4 ),
                'INIT' : ( Character.setAttribute, 'Initiative', { }, 0 ),
                'SPEED' : ( Character.setAttribute, 'Movement Speed', { }, 30 ),
                }

if __name__ == "__main__":
    sword = Weapon( 'Sword', [ 'MELEE', 'SLASHING', 'PIERCING', 'CORPORIAL' ] )
    bow = Weapon( 'Bow', [ 'RANGE', 'PIERCING', 'CORPORIAL' ] )
    bob = D20Character( "Bob", { 'STR': 13, 'DEX':15, 'CON':12, 'INT':10, 'WIS':8, 'CHA':18 } )
    dexmod = ModifierFactory( "Cause", 2 )
    print "AC before Dex mod"
    print bob.AC
    dexmod.addTarget( bob.DEX, Conditions( ( ), "and" ) )
    bob.beginCombat( )
    print "After"
    print bob.AC
    print "ATT before weapon"
    print bob.ATT
    bob.attack( bob, sword )
    print "After Sword"
    print bob.ATT
    bob.unreadyWeapon( )
    print "Sword Removed"
    print bob.ATT
    bob.attack( bob, bow )
    print "With Bow"
    print bob.ATT
