from rep import *

class D20AbilityScore( Stat ):
    def __init__( self, name, number, conditions ):
        import math
        super( D20AbilityScore, self ).__init__( name, number, conditions )
        self.mod = lambda: int( math.floor( ( int( self ) - 10 ) / 2 ) )

class D20Character( Character ):

    def beginCombat( self ):
        self.DEX.mod.addTarget( self.AC, Conditions( ( ), "and" ) )

    def endCombat( self ):
        self.DEX.mod.removeTarget( self.AC )

    def readyWeapon( self, weapon ):
        #This will need fixing.  It's just for testing purposes.  FIXME
        self.ATT.situation = weapon

    def unreadyWeapon( self ):
        #This will need fixing.  It's just for testing purposes.  FIXME
        self.ATT.situation = None

    #Properties
    def setAbilityScore( self, tag, name, number, modsprovided=None ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = D20AbilityScore( name, number, self.conditions )

    attTypes = { 
                #Basic Attributes
                'STR' : ( setAbilityScore, 'Strength', { } ),
                'DEX' : ( setAbilityScore, 'Dexterity', { } ),
                'CON' : ( setAbilityScore, 'Constitution', { } ),
                'INT' : ( setAbilityScore, 'Intelligence', { } ),
                'WIS' : ( setAbilityScore, 'Wisdom', { } ),
                'CHA' : ( setAbilityScore, 'Charisma', { } ),
                #END Basic Attributes

                #Calculated Attributes
                'AC' : ( Character.setAttribute, 'Armor Class', { } ),
                'ATT' : ( Character.setAttribute, 'Attack Bonus', { 'STR': ( "MELEE IN SOURCE TYPES", "and" ), 'DEX': ( "RANGE IN SOURCE TYPES", "and" )  } ),
                'INIT' : ( Character.setAttribute, 'Initiative', { } ),
                'SPEED' : ( Character.setAttribute, 'Movement Speed', { } ),
                }

if __name__ == "__main__":
    class Source:
        pass
    class Weapon:
        def __init__( self ):
            self.SOURCE = Source( )
    sword = Weapon( )
    sword.SOURCE.TYPES = [ 'MELEE', 'SLASHING', 'PIERCING', 'CORPORIAL' ]
    bow = Weapon( )
    bow.SOURCE.TYPES = [ 'RANGE', 'PIERCING', 'CORPORIAL' ]
    bob = D20Character( "Bob", conditions )
    dexmod = ModifierFactory( "Cause", 2 )
    print "AC before Dex mod"
    print bob.AC
    dexmod.addTarget( bob.DEX, Conditions( ( ), "and" ) )
    bob.beginCombat( )
    print "After"
    print bob.AC
    print "ATT before weapon"
    print bob.ATT
    bob.readyWeapon( sword )
    print "After Sword"
    print bob.ATT
    bob.unreadyWeapon( )
    print "Sword Removed"
    print bob.ATT
    bob.readyWeapon( bow )
    print "With Bow"
    print bob.ATT
