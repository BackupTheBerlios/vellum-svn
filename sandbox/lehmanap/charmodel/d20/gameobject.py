from charmodel.generic.gameobject import Character, EquippedItem
from charmodel.generic.dict import LevelBox
from attribute import D20AbilityScore, D20Attribute, D20Critical, D20CritRange, D20Damage, D20DamageRange, D20Size, D20Stat
from generator import D20Attack, D20CharacterClass, D20Race

class D20Weapon( EquippedItem ):
    def __init__( self, damageroll, types, *args, **kwargs ):
        self.roll = damageroll
        super( D20Weapon, self ).__init__( *args, **kwargs )
        self.DAMAGE = D20Damage( damageroll, range=self.SIZE )
        self.CRITICAL = D20Critical( damageroll, lambda: int( self.CRIT_MULT ), range=self.SIZE )
        self.TYPES = types

    def __str__( self ):
        return "%s %s %s" % ( self.name, self.TYPES, self.SIZE )

    def ready( self, character ):
        character.BAB.mod.addTarget( self.ATT, '' )
        self.getAtt( character ).addTarget( self.ATT, 'ABILITY' )
        self.getDmg( character ).addTarget( self.DAMAGE, 'ABILITY' )
        self.getDmg( character ).addTarget( self.CRITICAL, 'ABILITY' )

    def unready( self, character ):
        character.BAB.mod.removeTarget( self.ATT )
        self.getAtt( character ).removeTarget( self.ATT )
        self.getDmg( character ).removeTarget( self.DAMAGE )

    def getAtt( self, character ):
        return character.STR.mod

    def getDmg( self, character ):
        return character.STR.mod

    def setSize( self, tag, name, letter, modsprovided=None ):
        try:
            self.attrs[ tag ].letter = letter
        except:
            self.attrs[ tag ] = D20DamageRange( letter, self.roll )

    def setAttribute( self, tag, name, number ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = D20Attribute( name, number )

    def setCritRange( self, tag, name, number ):
        self.attrs[ tag ] = D20CritRange( number )

    attTypes =    { 
                    'SIZE' : ( setSize, 'Size Category', ( ), 0 ),
                    'CRIT_RANGE' : ( setCritRange, 'Critical Hit Threat Range', ( ), (19,20) ),
                    'CRIT_MULT' : ( setAttribute, 'Critical Hit Multiplier', ( ), 2 ),
                    'ATT' : ( setAttribute, 'Attack Bonus', ( ), -4 ),
                }

class D20RangedWeapon( D20Weapon ):
    def getAtt( self, character ):
        return character.DEX.mod

class D20Character( Character ):
    def __init__( self, name, race, attrs=None ):
        super( D20Character, self ).__init__( name, attrs )
        self.levels = LevelBox( )
        self.race = race
        self.FEATS = { }
        self.unarmed = D20Weapon( '1d3', [ 'MELEE', 'UNARMED', 'CORPORIAL' ], 'Unarmed', 0, { 'SIZE':0 , 'WEIGHT': 0 }, 'A barroom tradition', { } )
        self.grapple = D20Weapon( '1d8', [ 'MELEE', 'GRAPPLE', 'CORPORIAL' ], 'Grappling', 0, { 'SIZE':0, 'WEIGHT': 0 }, 'A barroom tradition', { } )
        self.weapon = None

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
        self.DEX.mod.addTarget( self.AC, 'ATTRIBUTE', ( ) )

    def endCombat( self ):
        self.DEX.mod.removeTarget( self.AC )

    def attack( self, foe, weapon=None ):
        #This will need fixing.  It's just for testing purposes.  FIXME
        if weapon:
            self.unreadyWeapon( )
            self.readyWeapon( weapon )
        weapon = self.weapon
        return D20Attack( None, self, foe )

    def readyWeapon( self, weapon ):
        weapon.ready( self )
        self.weapon = weapon

    def unreadyWeapon( self ):
        #This will need fixing.  It's just for testing purposes.  FIXME
        try:
            try:
                self.weapon.unready( self )
            except TypeError:
                pass
            if self.weapon != self.unarmed:
                self.readyWeapon( self.unarmed )
            else:
                self.weapon = None
        except AttributeError:
            pass

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

    def setStat( self, tag, name, number ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = D20Stat( name, number )

    def setSize( self, tag, name, letter, modsprovided=None ):
        try:
            self.attrs[ tag ].letter = letter
        except:
            self.attrs[ tag ] = D20Size( letter )

    def getATT( self ):
        try:
            return self.weapon.ATT
        except AttributeError:
            return self.BAB
    ATT = property( fget=getATT, doc="This character's Attack bonus" )

    def getLevel( self ):
        charlevelnum = 1
        try:
            for level in self.levels[ 'RACE' ].values( ):
                if level.enabled:
                    charlevelnum += 1
        except KeyError:
            pass
        return charlevelnum
    level = property( fget=getLevel, doc="This character's level" )

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
                'BAB' : ( setStat, 'Base Attack Bonus', ( ), 0 ),
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
                'EL' : ( setAttribute, 'Effective Level', ( ), 0 ),
                'HP' : ( setAttribute, 'Hit Points', ( ), 0 ),
                'WOUNDS' : ( setAttribute, 'Wounds', ( ), 0 ),
                'SPEED' : ( setAttribute, 'Movement Speed', ( ), 30 ),
                'SIZE' : ( setSize, 'Size Category', ( ), 'M' )
                }

if __name__ == "__main__":
    from charmodel.generic.gameobject import Item
    sword = D20Weapon( '1d8', [ 'MELEE', 'SLASHING', 'PIERCING', 'CORPORIAL' ], 'Longsword', 15, { 'WEIGHT':4, 'HEIGHT':18, 'WIDTH':4, 'DEPTH':2, 'SIZE':0 }, 'A sturdy longsword', { } )
    bow = D20RangedWeapon( '1d10', [ 'RANGE', 'PIERCING', 'CORPORIAL' ], 'Heavy Cross Bow', 50, { 'WEIGHT':8, 'HEIGHT':12, 'WIDTH':30, 'DEPTH':6, 'SIZE':0 }, 'A heavy crossbow', { } )
    race = D20Race( 'Elf', None, 
                {
                    'DEX': [ 2 ] + [ 0 ] * 19,
                    'CON': [ -2 ] + [ 0 ] * 19
                }, { } )
    bob = D20Character( "Bob", race, { 'STR': 150, 'DEX':15, 'CON':12, 'INT':10, 'WIS':8, 'CHA':18, 'HEIGHT':72, 'WEIGHT':221, 'WIDTH':24, 'DEPTH':12 } )
    charclass = D20CharacterClass( 'Fighter', None, 20, [ "10" ] * 20,
                { 
                    'BAB': [ 1 ] * 20,
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
    print int( bob.ATT )
    bob.readyWeapon( sword )
    att = bob.attack( bob )
    dmg = att.resolve( 19, 2 )
    bob.attack( bob, sword )
    print "After Sword"
    print int( bob.ATT )
    print "Sword Removed"
    print int( bob.ATT )
    bob.attack( bob, bow )
    print "With Bow"
    print bob.ATT
    strstone = Item( 'Strength Stone', 0, { 'WEIGHT':5, 'HEIGHT':6, 'WIDTH':6, 'DEPTH':6 }, 'A plain round stone', { 'CARRIER' : { 'STR' : ( 2, '' ) } } )
    strstone2 = Item( 'Strength Stone2', 0, { 'WEIGHT':5, 'HEIGHT':6, 'WIDTH':6, 'DEPTH':6 }, 'A plain round stone', { 'CARRIER' : { 'STR' : ( 5, '' ) } } )
    print "Sword + Strength Stone"
    bob.attack( bob, sword )
    bob.carry( strstone )
    print bob.ATT
    print "Sword + Strength Stone + Strength Stone 2"
    bob.attack( bob, sword )
    bob.carry( strstone2 )
    print bob.ATT
    bob.attack( bob, bob.grapple )
    print "Grappling"
    print int( bob.ATT )
    print bob.WILL
    print bob.FORT
    print bob.REF
